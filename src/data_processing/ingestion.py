import os
import requests
import pandas as pd
from bs4 import BeautifulSoup
from typing import List, Dict
import feedparser

class DataIngestion:
    def __init__(self):
        self.data_dir = "data"
        os.makedirs(f"{self.data_dir}/datasets", exist_ok=True)
        os.makedirs(f"{self.data_dir}/scraped", exist_ok=True)
    
    def download_kaggle_dataset(self, dataset_name: str) -> str:
        """Download policy dataset from Kaggle (placeholder)"""
        # In real implementation, use kaggle API
        print(f"Downloading {dataset_name} from Kaggle...")
        return f"{self.data_dir}/datasets/{dataset_name}.csv"
    
    def scrape_federal_register(self, limit: int = 100) -> List[Dict]:
        """Scrape recent Federal Register documents"""
        url = "https://www.federalregister.gov/documents.json"
        params = {'per_page': limit, 'order': 'newest'}
        
        try:
            response = requests.get(url, params=params)
            response.raise_for_status()
            documents = response.json().get('results', [])
            
            # Save to file
            df = pd.DataFrame(documents)
            df.to_csv(f"{self.data_dir}/scraped/federal_register.csv", index=False)
            
            return documents
        except Exception as e:
            print(f"Error scraping Federal Register: {e}")
            return []
    
    def scrape_epa_regulations(self) -> List[Dict]:
        """Scrape EPA regulations"""
        url = "https://www.epa.gov/laws-regulations"
        
        try:
            response = requests.get(url)
            response.raise_for_status()
            soup = BeautifulSoup(response.content, 'html.parser')
            
            regulations = []
            # Extract regulation links and titles
            for link in soup.find_all('a', href=True):
                if 'regulation' in link.get('href', '').lower():
                    regulations.append({
                        'title': link.text.strip(),
                        'url': link['href'],
                        'source': 'EPA'
                    })
            
            # Save to file
            df = pd.DataFrame(regulations)
            df.to_csv(f"{self.data_dir}/scraped/epa_regulations.csv", index=False)
            
            return regulations
        except Exception as e:
            print(f"Error scraping EPA: {e}")
            return []
    
    def load_sample_policy_data(self) -> pd.DataFrame:
        """Load sample policy data for testing"""
        sample_data = [
            {
                'policy_id': 'EO-14067',
                'title': 'Executive Order on Digital Assets',
                'type': 'Executive Order',
                'status': 'Active',
                'effective_date': '2022-03-09',
                'agency': 'White House',
                'summary': 'Framework for responsible development of digital assets'
            },
            {
                'policy_id': 'GDPR',
                'title': 'General Data Protection Regulation',
                'type': 'Regulation',
                'status': 'Active',
                'effective_date': '2018-05-25',
                'agency': 'EU',
                'summary': 'Data protection and privacy regulation'
            }
        ]
        
        df = pd.DataFrame(sample_data)
        df.to_csv(f"{self.data_dir}/sample_policies.csv", index=False)
        return df