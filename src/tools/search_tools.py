# src/tools/search_tools.py

import os
import requests
import time
from typing import List, Dict, Optional
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from src.utils.redis_cache import RedisCache

load_dotenv()

class SearchTools:
    """Direct web scraping tools for MARVEL TRL assessment"""
    
    def __init__(self):
        self.cache = RedisCache()
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
    
    def search_web_direct(self, query: str, num_results: int = 10) -> List[Dict]:
        """
        Direct web search without API (DuckDuckGo or similar)
        Free alternative to Google Custom Search
        """
        # Check cache
        cached = self.cache.get_search_results(query, "web_direct")
        if cached:
            print(f"✓ Using cached web results for: {query}")
            return cached
        
        try:
            # Using DuckDuckGo as a free alternative
            from duckduckgo_search import DDGS
            
            results = []
            with DDGS() as ddgs:
                for r in ddgs.text(query, max_results=num_results):
                    results.append({
                        "title": r.get("title", ""),
                        "url": r.get("href", ""),
                        "snippet": r.get("body", ""),
                        "source": "Web"
                    })
            
            self.cache.cache_search_results(query, "web_direct", results)
            print(f"✓ Web search: {len(results)} results for '{query}'")
            return results
            
        except ImportError:
            print("⚠ Install duckduckgo-search: pip install duckduckgo-search")
            return []
        except Exception as e:
            print(f"✗ Web search failed: {e}")
            return []
        
    def search_osti(self, query: str, num_results: int = 10) -> List[Dict]:
            """
            Search OSTI.gov for DOE technical reports
            """
            # Check cache
            cached = self.cache.get_search_results(query, "osti")
            if cached:
                print(f"✓ Using cached OSTI results for: {query}")
                return cached
            
            base_url = "https://www.osti.gov/api/v1/records"
            params = {
                "q": query,
                "page_size": num_results,
                "sort": "publication_date desc"
            }
            
            try:
                response = requests.get(base_url, params=params, timeout=10)
                response.raise_for_status()
                data = response.json()
                
                # FIX: Check if response is a list or dict
                if isinstance(data, list):
                    records = data
                elif isinstance(data, dict):
                    records = data.get("records", [])
                else:
                    print(f"⚠ Unexpected OSTI response format: {type(data)}")
                    return []
                
                results = []
                for record in records:
                    # Handle both dict and potentially other formats
                    if isinstance(record, dict):
                        results.append({
                            "title": record.get("title", "No title"),
                            "url": record.get("url", ""),
                            "snippet": str(record.get("description", ""))[:300],
                            "publication_date": record.get("publication_date", ""),
                            "authors": ", ".join(record.get("authors", [])) if isinstance(record.get("authors"), list) else str(record.get("authors", "")),
                            "source": "OSTI"
                        })
                
                self.cache.cache_search_results(query, "osti", results)
                print(f"✓ OSTI search: {len(results)} results for '{query}'")
                return results
                
            except Exception as e:
                print(f"✗ OSTI search failed: {e}")
                import traceback
                traceback.print_exc()  # Show full error for debugging
                return []        
    def search_arxiv(self, query: str, num_results: int = 10) -> List[Dict]:
        """
        Search arXiv for academic papers
        """
        # Check cache
        cached = self.cache.get_search_results(query, "arxiv")
        if cached:
            print(f"✓ Using cached arXiv results for: {query}")
            return cached
        
        try:
            import arxiv
            
            search = arxiv.Search(
                query=query,
                max_results=num_results,
                sort_by=arxiv.SortCriterion.Relevance
            )
            
            results = []
            for paper in search.results():
                results.append({
                    "title": paper.title,
                    "url": paper.entry_id,
                    "snippet": paper.summary[:300],
                    "publication_date": paper.published.strftime("%Y-%m-%d"),
                    "authors": ", ".join([a.name for a in paper.authors]),
                    "source": "arXiv"
                })
            
            self.cache.cache_search_results(query, "arxiv", results)
            print(f"✓ arXiv search: {len(results)} results for '{query}'")
            return results
            
        except Exception as e:
            print(f"✗ arXiv search failed: {e}")
            return []
    
    def search_inl_site(self, query: str, num_results: int = 10) -> List[Dict]:
        """
        Search INL website using Google Custom Search with site: filter
        """
        site_query = f"{query} site:inl.gov"
        return self.search_google_custom(site_query, num_results)
    
    def fetch_page_content(self, url: str) -> Optional[str]:
        """
        Fetch full text content from a URL
        """
        # Check cache
        cached = self.cache.get_search_results(url, "page_content")
        if cached:
            return cached[0].get("content")
        
        try:
            response = requests.get(url, headers=self.headers, timeout=15)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Remove script and style elements
            for script in soup(["script", "style"]):
                script.decompose()
            
            # Get text
            text = soup.get_text()
            
            # Clean up whitespace
            lines = (line.strip() for line in text.splitlines())
            chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
            text = '\n'.join(chunk for chunk in chunks if chunk)
            
            # Cache the content
            self.cache.cache_search_results(url, "page_content", [{"content": text}])
            
            return text
            
        except Exception as e:
            print(f"✗ Failed to fetch {url}: {e}")
            return None


class MARVELSearcherSimple:
    """
    Simplified searcher using only OSTI and arXiv (both free, no API keys)
    """
    
    def __init__(self):
        self.tools = SearchTools()
    
    def search_subsystem(self, subsystem_key: str, subsystem_config: dict) -> Dict:
        """
        Search using only free sources: OSTI + arXiv
        """
        print(f"\n{'='*60}")
        print(f"Searching for: {subsystem_config['name']}")
        print(f"{'='*60}\n")
        
        all_results = {
            "subsystem": subsystem_key,
            "name": subsystem_config['name'],
            "osti_results": [],
            "arxiv_results": [],
            "total_documents": 0
        }
        
        # Build search queries
        subsystem_terms = subsystem_config["key_terms"]
        
        # Search OSTI (covers TRL 4-7)
        print("🔍 Searching OSTI.gov (DOE technical reports)...")
        osti_queries = [
            f"MARVEL {subsystem_terms[0]}",
            f"MARVEL microreactor {subsystem_terms[1]}" if len(subsystem_terms) > 1 else f"MARVEL {subsystem_terms[0]}",
            f"microreactor {subsystem_terms[0]} testing"
        ]
        
        for query in osti_queries:
            results = self.tools.search_osti(query, 10)
            all_results["osti_results"].extend(results)
            time.sleep(2)
        
        print(f"  → Found {len(all_results['osti_results'])} OSTI documents")
        
        # Search arXiv (covers TRL 1-3)
        print("🔍 Searching arXiv (academic papers)...")
        arxiv_queries = [
            f"{subsystem_terms[0]} microreactor",
            f"{subsystem_terms[0]} small modular reactor",
            f"heat pipe reactor {subsystem_terms[0]}" if "heat" not in subsystem_terms[0].lower() else f"nuclear {subsystem_terms[0]}"
        ]
        
        for query in arxiv_queries:
            results = self.tools.search_arxiv(query, 5)
            all_results["arxiv_results"].extend(results)
            time.sleep(2)
        
        print(f"  → Found {len(all_results['arxiv_results'])} arXiv documents")
        
        all_results["total_documents"] = len(all_results["osti_results"]) + len(all_results["arxiv_results"])
        
        print(f"\n✅ Total documents found: {all_results['total_documents']}")
        
        return all_results