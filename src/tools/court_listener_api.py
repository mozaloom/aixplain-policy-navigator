import requests
from typing import Dict, List, Optional

class CourtListenerAPI:
    def __init__(self, api_key: Optional[str] = None):
        self.base_url = "https://www.courtlistener.com/api/rest/v4"
        self.headers = {}
        if api_key:
            self.headers['Authorization'] = f'Token {api_key}'
    
    def search_opinions(self, query: str, limit: int = 10) -> List[Dict]:
        """Search court opinions"""
        url = f"{self.base_url}/search/"
        params = {
            'q': query,
            'type': 'o',  # opinions
            'format': 'json',
            'order_by': 'score desc'
        }
        
        try:
            response = requests.get(url, params=params, headers=self.headers)
            response.raise_for_status()
            data = response.json()
            return data.get('results', [])[:limit]
        except Exception as e:
            print(f"Error searching CourtListener: {e}")
            return []
    
    def get_case_law_for_policy(self, policy_name: str) -> List[Dict]:
        """Get case law related to a specific policy"""
        cases = self.search_opinions(policy_name, limit=5)
        
        formatted_cases = []
        for case in cases:
            formatted_cases.append({
                'case_name': case.get('caseName', 'Unknown'),
                'court': case.get('court', 'Unknown Court'),
                'date_filed': case.get('dateFiled'),
                'snippet': case.get('snippet', ''),
                'url': f"https://www.courtlistener.com{case.get('absolute_url', '')}"
            })
        
        return formatted_cases