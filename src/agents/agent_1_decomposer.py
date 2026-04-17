from typing import List, Dict, Optional
import anthropic
from langchain_anthropic import ChatAnthropic
from langchain.prompts import ChatPromptTemplate
import networkx as nx
from src.models.ontology import (
    Ontology, OntologyNode, OntologyEdge,
    NodeType, Criticality, DependencyType
)
from src.config import UNIVERSAL_TAXONOMY, REACTOR_CONFIGS, DEPENDENCY_RULES
from src.apis.osti_client import OSTIClient
from src.utils.pdf_parser import extract_text_from_pdf
import os

class TechnologyDecomposer:
    """
    Agent 1: Extracts architecture from documents and builds ontology graph.
    """
    
    def __init__(self, api_key: str):
        self.llm = ChatAnthropic(
            model="claude-sonnet-4-20250514",
            api_key=api_key,
            temperature=0  # Deterministic for consistency
        )
        self.osti_client = OSTIClient()
    
    def decompose_reactor(self, reactor_name: str) -> Ontology:
        """
        Main entry point: Build complete ontology for a reactor.
        
        Steps:
        1. Fetch technical documents
        2. Extract architecture information
        3. Map to universal taxonomy
        4. Infer dependencies
        5. Build graph
        """
        print(f"🏗️  Starting decomposition for {reactor_name}...")
        
        # Step 1: Get reactor config
        config = REACTOR_CONFIGS.get(reactor_name.upper())
        if not config:
            raise ValueError(f"Unknown reactor: {reactor_name}")
        
        # Step 2: Fetch technical documents
        documents = self._fetch_documents(reactor_name)
        print(f"📄 Found {len(documents)} technical documents")
        
        # Step 3: Extract component list from documents
        components = self._extract_components(documents, reactor_name, config)
        print(f"🔍 Extracted {len(components)} components")
        
        # Step 4: Map to universal taxonomy (create nodes)
        nodes = self._create_nodes(components, reactor_name, config)
        print(f"📊 Created {len(nodes)} ontology nodes")
        
        # Step 5: Infer dependencies (create edges)
        edges = self._infer_dependencies(nodes, documents)
        print(f"🔗 Inferred {len(edges)} dependency edges")
        
        # Step 6: Build ontology
        ontology = Ontology(
            reactor=reactor_name,
            nodes=nodes,
            edges=edges,
            metadata={
                "config": config,
                "document_count": len(documents),
                "created_by": "Agent_1_Decomposer"
            }
        )
        
        print(f"✅ Ontology complete: {len(nodes)} nodes, {len(edges)} edges")
        return ontology
    
    def _fetch_documents(self, reactor_name: str) -> List[Dict]:
        """
        Fetch technical specifications from OSTI.
        Returns list of document metadata + text.
        """
        # Search OSTI for reactor technical docs
        query = f"{reactor_name} reactor technical specifications"
        results = self.osti_client.search(query, max_results=5)
        
        documents = []
        for result in results:
            # Download PDF if available
            if result.get('pdf_url'):
                pdf_path = self._download_pdf(result['pdf_url'], result['osti_id'])
                text = extract_text_from_pdf(pdf_path)
                result['full_text'] = text
            
            documents.append(result)
        
        return documents
    
    def _extract_components(
        self, 
        documents: List[Dict], 
        reactor_name: str,
        config: Dict
    ) -> List[Dict]:
        """
        Use LLM to extract component/subsystem mentions from documents.
        """
        # Combine document texts
        combined_text = "\n\n".join([
            doc.get('full_text', doc.get('abstract', ''))[:5000]  # Limit per doc
            for doc in documents
        ])
        
        prompt = ChatPromptTemplate.from_messages([
            ("system", """You are a nuclear engineering expert extracting system architecture.
            
Your task: Extract ALL subsystems and components mentioned in the technical documents.

Output format (JSON list):
[
    {
        "name": "HALEU Metallic Fuel",
        "type": "component",
        "subsystem": "Reactor Core & Fuel Assembly",
        "description": "Uranium-zirconium metallic alloy fuel enriched to 19.75%",
        "mentions": 5
    },
    ...
]

Be comprehensive but avoid duplicates. Normalize terminology (e.g., "heat pipe" = "thermal transfer pipe").
"""),
            ("user", """Reactor: {reactor_name}
Key features: {key_features}

Technical documents:
{documents}

Extract all components and subsystems.""")
        ])
        
        response = self.llm.invoke(
            prompt.format_messages(
                reactor_name=reactor_name,
                key_features=", ".join(config['key_features']),
                documents=combined_text[:15000]  # Claude context limit
            )
        )
        
        # Parse LLM response (should be JSON)
        import json
        try:
            components = json.loads(response.content)
        except json.JSONDecodeError:
            # Fallback: extract JSON from markdown code block
            import re
            json_match = re.search(r'```json\n(.*?)\n```', response.content, re.DOTALL)
            if json_match:
                components = json.loads(json_match.group(1))
            else:
                raise ValueError("LLM did not return valid JSON")
        
        return components
    
    def _create_nodes(
        self, 
        components: List[Dict], 
        reactor_name: str,
        config: Dict
    ) -> List[OntologyNode]:
        """
        Convert extracted components into OntologyNode objects.
        Map to universal taxonomy.
        """
        nodes = []
        
        # First, create subsystem nodes (from universal taxonomy)
        for subsystem_id, subsystem_data in UNIVERSAL_TAXONOMY.items():
            node = OntologyNode(
                id=f"{reactor_name.lower()}_{subsystem_id}",
                name=subsystem_data['name'],
                type=NodeType.SUBSYSTEM,
                parent_id=None,  # Top-level
                reactor=reactor_name,
                criticality=Criticality.HIGH,  # All subsystems are critical
                tags=[subsystem_id],
                description=subsystem_data['description']
            )
            nodes.append(node)
        
        # Then, create component nodes
        for idx, comp in enumerate(components):
            # Determine which subsystem this belongs to
            subsystem_id = self._map_to_subsystem(comp['subsystem'])
            
            node = OntologyNode(
                id=f"{reactor_name.lower()}_comp_{idx}_{comp['name'].lower().replace(' ', '_')}",
                name=comp['name'],
                type=NodeType.COMPONENT,
                parent_id=f"{reactor_name.lower()}_{subsystem_id}",
                reactor=reactor_name,
                criticality=self._assess_criticality(comp, config),
                tags=comp.get('tags', []),
                description=comp.get('description', '')
            )
            nodes.append(node)
        
        return nodes
    
    def _map_to_subsystem(self, subsystem_name: str) -> str:
        """
        Map extracted subsystem name to universal taxonomy key.
        """
        # Simple string matching (could be enhanced with embeddings)
        mapping = {
            "reactor core": "reactor_core_fuel",
            "fuel": "reactor_core_fuel",
            "heat transport": "heat_transport",
            "cooling": "heat_transport",
            "control": "reactivity_control",
            "shutdown": "reactivity_control",
            "decay heat": "decay_heat_removal",
            "emergency": "decay_heat_removal",
            "instrumentation": "instrumentation_control",
            "sensor": "instrumentation_control",
            "containment": "structural_containment",
            "vessel": "structural_containment"
        }
        
        subsystem_lower = subsystem_name.lower()
        for key, taxonomy_id in mapping.items():
            if key in subsystem_lower:
                return taxonomy_id
        
        # Default
        return "structural_containment"
    
    def _assess_criticality(self, component: Dict, config: Dict) -> Criticality:
        """
        Determine if component is critical path.
        """
        # Check if component is a key feature
        if any(kf in component['name'].lower() for kf in config['key_features']):
            return Criticality.HIGH
        
        # Otherwise moderate
        return Criticality.MEDIUM
    
    def _infer_dependencies(
        self, 
        nodes: List[OntologyNode],
        documents: List[Dict]
    ) -> List[OntologyEdge]:
        """
        Infer dependency edges between nodes.
        Uses both rule-based and LLM-based inference.
        """
        edges = []
        edge_counter = 0
        
        # Step 1: Apply universal dependency rules
        for rule in DEPENDENCY_RULES:
            from_nodes = [n for n in nodes if rule['from'] in n.id]
            to_nodes = [n for n in nodes if rule['to'] in n.id]
            
            for from_node in from_nodes:
                for to_node in to_nodes:
                    edge = OntologyEdge(
                        id=f"edge_{edge_counter}",
                        from_node=from_node.id,
                        to_node=to_node.id,
                        dependency_type=DependencyType(rule['type']),
                        strength="strong",
                        description=rule['rationale']
                    )
                    edges.append(edge)
                    edge_counter += 1
        
        # Step 2: LLM-based inference for component-level dependencies
        # (Optional: for MVP, just use rules)
        
        return edges
    
    def _download_pdf(self, url: str, doc_id: str) -> str:
        """Download PDF and return local path."""
        import requests
        from pathlib import Path
        
        output_dir = Path("data/documents/osti")
        output_dir.mkdir(parents=True, exist_ok=True)
        
        filepath = output_dir / f"{doc_id}.pdf"
        
        if filepath.exists():
            return str(filepath)
        
        response = requests.get(url)
        with open(filepath, 'wb') as f:
            f.write(response.content)
        
        return str(filepath)