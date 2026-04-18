import requests
from typing import List, Dict, Optional

class OSTIClient:
    """
    Client for OSTI.gov API
    Docs: https://www.osti.gov/api/v1/docs
    """
    BASE_URL = "https://www.osti.gov/api/v1/records"
    
    def search(
        self, 
        query: str, 
        max_results: int = 10,
        year_start: Optional[int] = None
    ) -> List[Dict]:
        """
        Search OSTI database.
        
        Args:
            query: Search keywords
            max_results: Number of results to return
            year_start: Filter by publication year (e.g., 2018)
        
        Returns:
            List of document metadata dicts
        """
        params = {
            "search": query,
            "rows": max_results,
            "sort": "publication_date desc"
        }
        
        if year_start:
            params["publication_date"] = f"[{year_start} TO *]"
        
        try:
            response = requests.get(self.BASE_URL, params=params, timeout=30)
            response.raise_for_status()
            data = response.json()
            
            results = []
            for item in data.get('records', []):
                result = {
                    "osti_id": item.get('osti_id'),
                    "title": item.get('title'),
                    "abstract": item.get('abstract'),
                    "authors": item.get('authors', []),
                    "publication_date": item.get('publication_date'),
                    "url": item.get('url'),
                    "pdf_url": item.get('links', {}).get('fulltext'),
                    "document_type": item.get('product_type', 'technical_report')
                }
                results.append(result)
            
            return results
        
        except requests.RequestException as e:
            print(f"❌ OSTI API error: {e}")
            return []