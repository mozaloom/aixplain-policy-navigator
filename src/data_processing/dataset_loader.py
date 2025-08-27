import os
import pandas as pd
import requests
from typing import Dict, List
from .vector_store import VectorStoreManager

class DatasetLoader:
    def __init__(self, vector_store: VectorStoreManager):
        self.vector_store = vector_store
        self.loaded_datasets = []
    
    def load_sample_policy_dataset(self) -> Dict:
        """Load sample policy dataset"""
        # Create sample policy data
        sample_policies = [
            {
                "title": "General Data Protection Regulation (GDPR)",
                "content": "The General Data Protection Regulation (GDPR) is a regulation in EU law on data protection and privacy in the European Union and the European Economic Area. It addresses the transfer of personal data outside the EU and EEA areas. Small businesses with fewer than 250 employees have simplified reporting requirements but must still comply with core GDPR principles.",
                "type": "privacy_law",
                "jurisdiction": "EU",
                "effective_date": "2018-05-25"
            },
            {
                "title": "Executive Order 14067 - Digital Assets",
                "content": "Executive Order 14067, titled 'Ensuring Responsible Development of Digital Assets,' was signed on March 9, 2022. This order establishes the first-ever, whole-of-Government approach to addressing the risks and harnessing the potential benefits of digital assets and their underlying technology.",
                "type": "executive_order",
                "jurisdiction": "US",
                "effective_date": "2022-03-09"
            },
            {
                "title": "Section 230 Communications Decency Act",
                "content": "Section 230 of the Communications Decency Act provides immunity to online platforms from liability for user-generated content. It has been subject to various court challenges, including Fair Housing Council v. Roommates.com, which clarified limits on platform immunity.",
                "type": "federal_law",
                "jurisdiction": "US",
                "effective_date": "1996-02-08"
            }
        ]
        
        indexed_count = 0
        for policy in sample_policies:
            doc_id = self.vector_store.add_document(
                policy["content"],
                {
                    "source": "sample_dataset",
                    "title": policy["title"],
                    "type": policy["type"],
                    "jurisdiction": policy["jurisdiction"],
                    "effective_date": policy["effective_date"]
                }
            )
            indexed_count += 1
        
        self.loaded_datasets.append("sample_policy_dataset")
        
        return {
            "dataset": "sample_policy_dataset",
            "documents_indexed": indexed_count,
            "status": "loaded"
        }
    
    def load_government_websites(self) -> Dict:
        """Load content from government websites"""
        gov_urls = [
            "https://www.federalregister.gov/",
            "https://www.epa.gov/laws-regulations",
            "https://www.cdc.gov/policy/"
        ]
        
        indexed_count = 0
        errors = []
        
        for url in gov_urls:
            try:
                result = self.vector_store.index_url(url)
                if result["status"] == "indexed":
                    indexed_count += 1
                else:
                    errors.append(result)
            except Exception as e:
                errors.append({"url": url, "error": str(e)})
        
        self.loaded_datasets.append("government_websites")
        
        return {
            "dataset": "government_websites",
            "urls_processed": len(gov_urls),
            "documents_indexed": indexed_count,
            "errors": errors,
            "status": "loaded"
        }
    
    def load_csv_dataset(self, file_path: str) -> Dict:
        """Load policy data from CSV file"""
        try:
            df = pd.read_csv(file_path)
            indexed_count = 0
            
            for _, row in df.iterrows():
                content = " ".join([str(val) for val in row.values if pd.notna(val)])
                
                doc_id = self.vector_store.add_document(
                    content,
                    {
                        "source": "csv_dataset",
                        "file_path": file_path,
                        "type": "structured_data",
                        "row_data": row.to_dict()
                    }
                )
                indexed_count += 1
            
            self.loaded_datasets.append(f"csv_{os.path.basename(file_path)}")
            
            return {
                "dataset": f"csv_{os.path.basename(file_path)}",
                "documents_indexed": indexed_count,
                "status": "loaded"
            }
            
        except Exception as e:
            return {
                "dataset": file_path,
                "status": "error",
                "error": str(e)
            }
    
    def get_loaded_datasets(self) -> List[str]:
        """Get list of loaded datasets"""
        return self.loaded_datasets