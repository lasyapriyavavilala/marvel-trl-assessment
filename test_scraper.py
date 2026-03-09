# test_scraper.py - Updated

from src.tools.search_tools import MARVELSearcherSimple  # Use simple version
from config.subsystems import MARVEL_SUBSYSTEMS
import json
import os

def test_single_subsystem():
    """Test scraping for heat transport system"""
    
    # Create output directory
    os.makedirs("data/raw", exist_ok=True)
    
    searcher = MARVELSearcherSimple()
    
    # Search just heat transport
    results = searcher.search_subsystem(
        "heat_transport",
        MARVEL_SUBSYSTEMS["heat_transport"]
    )
    
    # Save results
    with open("data/raw/heat_transport_results.json", "w") as f:
        json.dump(results, f, indent=2)
    
    print("\n" + "="*60)
    print("SUMMARY")
    print("="*60)
    print(f"Subsystem: {results['name']}")
    print(f"Total documents: {results['total_documents']}")
    print(f"\nBreakdown by source:")
    print(f"  OSTI: {len(results['osti_results'])} documents")
    print(f"  arXiv: {len(results['arxiv_results'])} documents")
    
    # Show sample results
    if results['osti_results']:
        print(f"\n📄 Sample OSTI result:")
        sample = results['osti_results'][0]
        print(f"   Title: {sample['title']}")
        print(f"   URL: {sample.get('url', 'No URL')}")
        print(f"   Date: {sample.get('publication_date', 'No date')}")
    
    if results['arxiv_results']:
        print(f"\n📄 Sample arXiv result:")
        sample = results['arxiv_results'][0]
        print(f"   Title: {sample['title']}")
        print(f"   URL: {sample['url']}")

if __name__ == "__main__":
    print("MARVEL TRL Assessment - Simplified Scraping Test")
    print("Using only free APIs: OSTI + arXiv")
    print("="*60)
    
    test_single_subsystem()