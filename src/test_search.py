# test_search.py

"""
Quick test script to verify setup
"""

from src.agents.search_agent import SearchAgent
from src.utils.redis_cache import RedisCache
import os
from dotenv import load_dotenv

def test_setup():
    """Test that everything is configured correctly"""
    
    print("=== Testing Setup ===\n")
    
    # 1. Check environment variables
    load_dotenv()
    print("✓ .env file loaded")
    
    anthropic_key = os.getenv("ANTHROPIC_API_KEY")
    if anthropic_key and len(anthropic_key) > 10:
        print("✓ Anthropic API key found")
    else:
        print("✗ Anthropic API key missing or invalid")
        return False
    
    # 2. Check Redis
    try:
        cache = RedisCache()
        cache.client.ping()
        print("✓ Redis connection successful")
    except Exception as e:
        print(f"✗ Redis connection failed: {e}")
        return False
    
    # 3. Test search tools
    print("\n=== Testing Search Tools ===\n")
    from src.tools.search_tools import SearchTools
    
    # Test OSTI search
    print("Testing OSTI search...")
    osti_results = SearchTools.search_osti("MARVEL microreactor")
    if osti_results and "error" not in osti_results[0]:
        print(f"✓ OSTI search working ({len(osti_results)} results)")
    else:
        print(f"✗ OSTI search failed: {osti_results}")
    
    # Test arXiv search
    print("Testing arXiv search...")
    arxiv_results = SearchTools.search_arxiv("microreactor heat pipe")
    if arxiv_results and "error" not in arxiv_results[0]:
        print(f"✓ arXiv search working ({len(arxiv_results)} results)")
    else:
        print(f"✗ arXiv search failed: {arxiv_results}")
    
    print("\n=== Setup Complete ===")
    return True

def test_search_agent():
    """Test the search agent on one subsystem"""
    
    print("\n=== Testing Search Agent ===\n")
    print("Searching for MARVEL heat transport system documentation...")
    print("(This may take 1-2 minutes)\n")
    
    agent = SearchAgent()
    results = agent.search_subsystem("heat_transport")
    
    print("\n=== Results ===")
    print(f"Status: {results['status']}")
    print(f"\nAgent Output:\n{results['search_output'][:500]}...")
    
    return results

if __name__ == "__main__":
    # First test setup
    if test_setup():
        # Then test search agent
        response = input("\nRun full search agent test? (y/n): ")
        if response.lower() == 'y':
            test_search_agent()