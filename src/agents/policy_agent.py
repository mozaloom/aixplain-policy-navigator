import os
from typing import Dict, List, Any
from aixplain.factories import AgentFactory
from aixplain.modules.agent.tool.model_tool import ModelTool
from aixplain.modules.agent.agent_task import AgentTask
from ..utils.config import CONFIG
from ..tools.custom_tools import PolicyStatusChecker, ComplianceAnalyzer, PolicySearchTool
from ..tools.external_integrations import ExternalToolManager
from ..data_processing.vector_store import VectorStoreManager
from ..data_processing.dataset_loader import DatasetLoader

class PolicyNavigatorAgent:
    def __init__(self):
        self.config = CONFIG
        self.policy_checker = PolicyStatusChecker()
        self.compliance_analyzer = ComplianceAnalyzer()
        self.search_tool = PolicySearchTool()
        self.agent = None
        
        # Missing components from PDF requirements
        self.vector_store = VectorStoreManager()
        self.dataset_loader = DatasetLoader(self.vector_store)
        self.external_tools = ExternalToolManager()
        
        # Load initial datasets
        self._load_initial_data()
    
    def create_agent(self):
        """Create the main policy navigator agent"""
        
        # Define agent tasks
        policy_search_task = AgentTask(
            name="policy_search",
            description="Search and retrieve policy documents from various sources",
            expected_output="List of relevant policy documents with metadata"
        )
        
        status_check_task = AgentTask(
            name="status_check",
            description="Check the current status of policies and regulations",
            expected_output="Current status information with source verification"
        )
        
        compliance_task = AgentTask(
            name="compliance_analysis",
            description="Analyze compliance requirements for different business types",
            expected_output="Detailed compliance requirements and deadlines"
        )
        
        # Create tools
        tools = [
            # Document processor from marketplace
            ModelTool(model=self.config['tools']['document_processor']),
            
            # Web scraper tool
            ModelTool(model=self.config['tools']['web_scraper']),
            
            # Google search tool
            ModelTool(model=self.config['tools']['google_search']),
            
            # Python interpreter for custom analysis
            AgentFactory.create_python_interpreter_tool()
        ]
        
        # Create the agent
        self.agent = AgentFactory.create(
            name="Policy Navigator Agent",
            description="Expert agent for government regulation and compliance analysis",
            instructions="""
            You are a specialized agent for analyzing government regulations, policies, and compliance requirements.
            
            Your capabilities include:
            1. Searching Federal Register for policy documents
            2. Checking policy status and amendments
            3. Analyzing compliance requirements for different business sizes
            4. Retrieving related case law from court databases
            5. Providing actionable compliance guidance
            
            When answering queries:
            - Always verify information from official sources
            - Provide specific dates and reference numbers when available
            - Explain compliance requirements clearly for different business types
            - Include relevant deadlines and key requirements
            - Cite sources for all information provided
            """,
            tasks=[policy_search_task, status_check_task, compliance_task],
            tools=tools,
            llm_id=self.config['aixplain']['default_llm_id']
        )
        
        return self.agent
    
    def query(self, question: str, **kwargs):
        """Query the policy agent - let it decide what APIs to use"""
        if not self.agent:
            self.create_agent()
        
        try:
            response = self.agent.run(question, **kwargs)
            return response["data"]
        except Exception as e:
            return {
                "output": f"Error processing query: {str(e)}",
                "error": str(e)
            }
    
    def check_policy_status(self, policy_id: str):
        """Check specific policy status using real APIs"""
        result = self.policy_checker.check_policy_status(policy_id)
        return result
    
    def analyze_compliance(self, business_type: str, size: str):
        """Analyze compliance requirements with detailed response"""
        result = self.compliance_analyzer.analyze_compliance_requirements(business_type, size)
        
        # Format like PDF examples
        requirements_text = "\n".join([f"• {req}" for reqs in result['requirements'].values() for req in reqs])
        
        return {
            "output": f"Based on current regulations for {size} {business_type}:\n\n{requirements_text}\n\nCompliance deadlines: {', '.join(result['deadlines'])}\n\nSource: Government Compliance Database",
            "requirements": result['requirements'],
            "deadlines": result['deadlines']
        }
    
    def search_policies(self, query: str):
        """Search for policies"""
        return self.search_tool.search_policies(query)
    
    def deploy(self):
        """Deploy agent to cloud"""
        if self.agent:
            self.agent.deploy()
            return f"Policy Navigator Agent deployed with ID: {self.agent.id}"
        return "Agent not created yet"
    
    def _load_initial_data(self):
        """Load initial datasets as required by PDF"""
        try:
            # Load sample policy dataset
            self.dataset_loader.load_sample_policy_dataset()
            
            # Load government websites
            self.dataset_loader.load_government_websites()
            
            print("✅ Initial datasets loaded successfully")
        except Exception as e:
            print(f"⚠️ Dataset loading failed: {e}")
    
    def upload_document(self, file_path: str) -> Dict:
        """Upload and index policy document"""
        return self.vector_store.upload_document(file_path)
    
    def index_url(self, url: str) -> Dict:
        """Index content from government/regulatory URL"""
        return self.vector_store.index_url(url)
    
    def search_indexed_content(self, query: str) -> List[Dict]:
        """Search through indexed documents"""
        return self.vector_store.search_documents(query)
    
    def send_policy_alert(self, policy_info: Dict) -> Dict:
        """Send policy update to external tools (Slack/Notion/Calendar)"""
        return self.external_tools.handle_policy_update(policy_info)
    
    def get_system_stats(self) -> Dict:
        """Get comprehensive system statistics"""
        return {
            "vector_store": self.vector_store.get_document_stats(),
            "datasets": self.dataset_loader.get_loaded_datasets(),
            "agent_status": "active" if self.agent else "not_created"
        }