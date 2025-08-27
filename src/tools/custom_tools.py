import sqlite3
import pandas as pd
from typing import Dict, List, Any
from .federal_register_api import FederalRegisterAPI
from .court_listener_api import CourtListenerAPI

class PolicyStatusChecker:
    def __init__(self):
        self.federal_api = FederalRegisterAPI()
        self.court_api = CourtListenerAPI()
    
    def check_policy_status(self, policy_id: str) -> Dict[str, Any]:
        """Check comprehensive policy status"""
        federal_status = self.federal_api.check_policy_status(policy_id)
        case_law = self.court_api.get_case_law_for_policy(policy_id)
        
        return {
            "policy_id": policy_id,
            "federal_status": federal_status,
            "related_cases": case_law,
            "summary": f"Policy {policy_id} status: {federal_status.get('status', 'unknown')}"
        }

class ComplianceAnalyzer:
    def __init__(self, db_path: str = None):
        self.db_path = db_path or "data/compliance.db"
    
    def analyze_compliance_requirements(self, business_type: str, size: str) -> Dict[str, Any]:
        """Analyze compliance requirements for business type and size"""
        # Simplified compliance analysis
        requirements = {
            "small_business": {
                "gdpr": ["Data protection officer not required", "Simplified reporting"],
                "sox": ["Not applicable for private companies"],
                "ada": ["Website accessibility required"]
            },
            "large_business": {
                "gdpr": ["Data protection officer required", "Full compliance reporting"],
                "sox": ["Full compliance if public company"],
                "ada": ["Full accessibility compliance"]
            }
        }
        
        return {
            "business_type": business_type,
            "size": size,
            "requirements": requirements.get(size, {}),
            "deadlines": ["Annual review required", "Quarterly assessments"]
        }

class PolicySearchTool:
    def __init__(self):
        self.federal_api = FederalRegisterAPI()
    
    def search_policies(self, query: str, source: str = "federal") -> List[Dict]:
        """Search policies across different sources"""
        if source == "federal":
            return self.federal_api.search_documents(query)
        return []