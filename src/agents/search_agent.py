
from langchain.agents import AgentExecutor, create_react_agent
from langchain_anthropic import ChatAnthropic
from langchain.prompts import PromptTemplate
from src.tools.search_tools import create_search_tools
from src.utils.redis_cache import RedisCache
from config.subsystems import MARVEL_SUBSYSTEMS, SOURCE_MAPPING

class SearchAgent:
    """Search Agent for finding MARVEL reactor documentation"""
    
    def __init__(self):
        self.llm = ChatAnthropic(
            model="claude-sonnet-4-20250514",
            temperature=0
        )
        self.tools = create_search_tools()
        self.cache = RedisCache()
        
        # Create agent
        prompt = PromptTemplate.from_template("""
You are a Search Agent specializing in finding technical documentation for the MARVEL microreactor.

Your task: Find evidence for the {subsystem} subsystem.

Search Strategy (work backwards from highest TRL):
1. TRL 8-9: Search for operational evidence (first criticality, operational reports)
   - Tools: GoogleNews, INLSearch
   - Keywords: "MARVEL" + {subsystem_terms} + "operational" OR "first criticality"

2. TRL 6-7: Search for demonstration/licensing evidence
   - Tools: INLSearch
   - Keywords: "MARVEL" + {subsystem_terms} + "fabrication complete" OR "integration"

3. TRL 4-5: Search for testing/validation evidence
   - Tools: OSTISearch, INLSearch
   - Keywords: "MARVEL" + {subsystem_terms} + "prototype" OR "testing"

4. TRL 1-3: Search for conceptual design evidence
   - Tools: arXivSearch
   - Keywords: "microreactor" OR "heat pipe reactor" + {subsystem_terms} + "conceptual"

Key terms for {subsystem}: {subsystem_terms}

Available tools: {tools}

{agent_scratchpad}

Question: Find documentation for {subsystem} in MARVEL reactor. Start with TRL 8-9 sources.
""")
        
        self.agent = create_react_agent(self.llm, self.tools, prompt)
        self.executor = AgentExecutor(
            agent=self.agent,
            tools=self.tools,
            verbose=True,
            max_iterations=10
        )
    
    def search_subsystem(self, subsystem_key: str) -> dict:
        """
        Search for documentation on a specific subsystem
        
        Args:
            subsystem_key: Key from MARVEL_SUBSYSTEMS dict
            
        Returns:
            dict with search results
        """
        subsystem_config = MARVEL_SUBSYSTEMS[subsystem_key]
        
        # Check cache first
        cached_state = self.cache.get_subsystem_state(subsystem_key)
        if cached_state:
            print(f"Found cached results for {subsystem_key}")
            return cached_state
        
        # Run search
        result = self.executor.invoke({
            "subsystem": subsystem_config["name"],
            "subsystem_terms": ", ".join(subsystem_config["key_terms"]),
            "tools": "\n".join([f"- {t.name}: {t.description}" for t in self.tools])
        })
        
        # Cache results
        state = {
            "subsystem": subsystem_key,
            "search_output": result["output"],
            "status": "searched"
        }
        self.cache.save_subsystem_state(subsystem_key, state)
        
        return state

# Test the agent
if __name__ == "__main__":
    agent = SearchAgent()
    
    # Search for heat transport system
    results = agent.search_subsystem("heat_transport")
    print("\n=== SEARCH RESULTS ===")
    print(results)