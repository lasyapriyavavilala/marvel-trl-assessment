from pydantic import BaseModel, Field
from typing import List, Optional, Literal
from enum import Enum

class NodeType(str, Enum):
    SYSTEM = "system"
    SUBSYSTEM = "subsystem"
    COMPONENT = "component"

class Criticality(str, Enum):
    HIGH = "high"          # System can't operate without this
    MEDIUM = "medium"      # Degraded performance without this
    LOW = "low"            # Nice to have, but not essential

class DependencyType(str, Enum):
    STRUCTURAL = "structural"         # X contains Y
    FUNCTIONAL = "functional"         # X must work for Y to work
    THERMAL = "thermal_interface"     # Heat transfer
    ELECTRICAL = "electrical"         # Power transfer
    MECHANICAL = "mechanical"         # Physical connection
    INFORMATIONAL = "informational"   # Data/control signals
    SAFETY = "safety_backup"          # Y backs up X

class OntologyNode(BaseModel):
    id: str = Field(..., description="Unique identifier (e.g., 'marvel_haleu_fuel')")
    name: str = Field(..., description="Human-readable name")
    type: NodeType
    parent_id: Optional[str] = Field(None, description="Parent node ID")
    reactor: str = Field(..., description="Which reactor (MARVEL, KRONOS, eVinci)")
    criticality: Criticality = Criticality.MEDIUM
    tags: List[str] = Field(default_factory=list, description="Keywords for search")
    description: Optional[str] = None

class OntologyEdge(BaseModel):
    id: str = Field(..., description="Unique identifier")
    from_node: str = Field(..., description="Source node ID")
    to_node: str = Field(..., description="Target node ID")
    dependency_type: DependencyType
    strength: Literal["strong", "moderate", "weak"] = "moderate"
    description: Optional[str] = None

class Ontology(BaseModel):
    """Complete ontology for a reactor"""
    reactor: str
    nodes: List[OntologyNode]
    edges: List[OntologyEdge]
    metadata: dict = Field(default_factory=dict)
    
    def to_networkx(self):
        """Convert to NetworkX graph for algorithms"""
        import networkx as nx
        G = nx.DiGraph()
        
        for node in self.nodes:
            G.add_node(node.id, **node.dict())
        
        for edge in self.edges:
            G.add_edge(edge.from_node, edge.to_node, **edge.dict())
        
        return G
    
    def save(self, filepath: str):
        """Save ontology to JSON"""
        import json
        with open(filepath, 'w') as f:
            json.dump(self.dict(), f, indent=2)
    
    @classmethod
    def load(cls, filepath: str):
        """Load ontology from JSON"""
        import json
        with open(filepath, 'r') as f:
            data = json.load(f)
        return cls(**data)