import os
import json
import requests
from typing import List, Dict, Any
import pandas as pd
from bs4 import BeautifulSoup

class VectorStoreManager:
    def __init__(self):
        self.documents = []
        self.embeddings = {}
        self.indexed_urls = set()
    
    def add_document(self, content: str, metadata: Dict) -> str:
        """Add document to vector store"""
        doc_id = f"doc_{len(self.documents)}"
        
        document = {
            "id": doc_id,
            "content": content,
            "metadata": metadata,
            "indexed_at": pd.Timestamp.now().isoformat()
        }
        
        self.documents.append(document)
        return doc_id
    
    def index_url(self, url: str) -> Dict:
        """Index content from URL"""
        if url in self.indexed_urls:
            return {"status": "already_indexed", "url": url}
        
        try:
            response = requests.get(url, timeout=10)
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Extract text content
            content = soup.get_text()
            title = soup.find('title').text if soup.find('title') else url
            
            doc_id = self.add_document(content, {
                "source": "url",
                "url": url,
                "title": title,
                "type": "web_content"
            })
            
            self.indexed_urls.add(url)
            
            return {
                "status": "indexed",
                "doc_id": doc_id,
                "url": url,
                "title": title
            }
            
        except Exception as e:
            return {"status": "error", "url": url, "error": str(e)}
    
    def upload_document(self, file_path: str, doc_type: str = "policy") -> Dict:
        """Upload and index document file"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            doc_id = self.add_document(content, {
                "source": "upload",
                "file_path": file_path,
                "type": doc_type,
                "filename": os.path.basename(file_path)
            })
            
            return {
                "status": "uploaded",
                "doc_id": doc_id,
                "filename": os.path.basename(file_path)
            }
            
        except Exception as e:
            return {"status": "error", "file_path": file_path, "error": str(e)}
    
    def search_documents(self, query: str, limit: int = 5) -> List[Dict]:
        """Search documents (simple text matching)"""
        results = []
        query_lower = query.lower()
        
        for doc in self.documents:
            if query_lower in doc["content"].lower():
                score = doc["content"].lower().count(query_lower)
                results.append({
                    "doc_id": doc["id"],
                    "content": doc["content"][:500] + "...",
                    "metadata": doc["metadata"],
                    "score": score
                })
        
        # Sort by relevance score
        results.sort(key=lambda x: x["score"], reverse=True)
        return results[:limit]
    
    def get_document_stats(self) -> Dict:
        """Get vector store statistics"""
        sources = {}
        for doc in self.documents:
            source = doc["metadata"].get("source", "unknown")
            sources[source] = sources.get(source, 0) + 1
        
        return {
            "total_documents": len(self.documents),
            "sources": sources,
            "indexed_urls": len(self.indexed_urls)
        }