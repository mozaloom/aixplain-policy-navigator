import requests
from typing import Dict, List, Optional

class FederalRegisterAPI:
    def __init__(self):
        self.base_url = "https://www.federalregister.gov/api/v1"
    
    def search_documents(self, query: str, limit: int = 10) -> List[Dict]:
        """Search Federal Register documents"""
        url = f"{self.base_url}/documents.json"
        params = {
            'conditions[term]': query,
            'per_page': limit,
            'fields[]': ['title', 'abstract', 'html_url', 'publication_date', 'type', 'agencies']
        }
        
        try:
            response = requests.get(url, params=params)
            response.raise_for_status()
            return response.json().get('results', [])
        except Exception as e:
            print(f"Error searching Federal Register: {e}")
            return []
    
    def get_document_by_number(self, document_number: str) -> Optional[Dict]:
        """Get specific document by Federal Register number"""
        url = f"{self.base_url}/documents/{document_number}.json"
        
        try:
            response = requests.get(url)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"Error fetching document {document_number}: {e}")
            return None
    
    def check_policy_status(self, policy_id: str) -> Dict:
        """Check if a policy is still in effect"""
        documents = self.search_documents(policy_id, limit=5)
        
        if not documents:
            return {"status": "not_found", "message": f"No documents found for {policy_id}"}
        
        # Look for the most recent document
        latest_doc = max(documents, key=lambda x: x.get('publication_date', ''))
        
        return {
            "status": "active",
            "title": latest_doc.get('title'),
            "publication_date": latest_doc.get('publication_date'),
            "url": latest_doc.get('html_url'),
            "type": latest_doc.get('type')
        }