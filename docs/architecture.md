# Policy Navigator Architecture

## System Overview

The Policy Navigator is a Multi-Agent RAG (Retrieval-Augmented Generation) system built with the aiXplain SDK that enables intelligent querying of government regulations, compliance policies, and public health guidelines.

## Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                        User Interfaces                          │
├─────────────────────┬─────────────────────┬─────────────────────┤
│   React Web App    │    CLI Interface    │    API Endpoints    │
│   (Frontend)       │   (Command Line)    │   (RESTful API)     │
└─────────────────────┴─────────────────────┴─────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────┐
│                      Flask API Server                          │
│                    (api_server.py)                             │
└─────────────────────────────────────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────┐
│                  Policy Navigator Agent                        │
│                 (Multi-Agent RAG Core)                         │
├─────────────────────┬─────────────────────┬─────────────────────┤
│   Agent Factory     │    Task Manager     │   Tool Orchestrator│
│   (aiXplain SDK)    │   (Query Routing)   │  (Tool Integration) │
└─────────────────────┴─────────────────────┴─────────────────────┘
                                │
                ┌───────────────┼───────────────┐
                ▼               ▼               ▼
┌─────────────────────┐ ┌─────────────────┐ ┌─────────────────────┐
│   Data Processing   │ │   Tool Layer    │ │ External Integration│
│                     │ │                 │ │                     │
│ • Vector Store      │ │ • Marketplace   │ │ • Slack Webhook     │
│ • Dataset Loader    │ │ • Custom Tools  │ │ • Notion API        │
│ • Document Indexer  │ │ • External APIs │ │ • Calendar API      │
│ • URL Scraper       │ │ • Code Interp.  │ │ • Alert System      │
└─────────────────────┘ └─────────────────┘ └─────────────────────┘
                                │
                ┌───────────────┼───────────────┐
                ▼               ▼               ▼
┌─────────────────────┐ ┌─────────────────┐ ┌─────────────────────┐
│   Data Sources      │ │   AI Models     │ │   External APIs     │
│                     │ │                 │ │                     │
│ • Sample Datasets   │ │ • GPT-4 (LLM)   │ │ • Federal Register  │
│ • Government URLs   │ │ • Doc Processor │ │ • CourtListener     │
│ • Uploaded Files    │ │ • Web Scraper   │ │ • EPA Regulations   │
│ • CSV/SQL Data      │ │ • Search Engine │ │ • CDC Policies      │
└─────────────────────┘ └─────────────────┘ └─────────────────────┘
```

## Core Components

### 1. Multi-Agent RAG System

#### Agent Factory (aiXplain SDK)
```python
self.agent = AgentFactory.create(
    name="Policy Navigator Agent",
    description="Expert agent for government regulation analysis",
    instructions="Specialized agent for policy analysis...",
    tasks=[policy_search_task, status_check_task, compliance_task],
    tools=[marketplace_tools, custom_tools, api_tools],
    llm_id="6646261c6eb563165658bbb1"  # GPT-4
)
```

#### Task Management
- **Policy Search Task**: Document retrieval and analysis
- **Status Check Task**: Real-time policy status verification
- **Compliance Task**: Business compliance requirement analysis

### 2. Data Processing Layer

#### Vector Store Manager
```python
class VectorStoreManager:
    def add_document(self, content: str, metadata: Dict) -> str
    def search_documents(self, query: str, limit: int = 5) -> List[Dict]
    def index_url(self, url: str) -> Dict
    def upload_document(self, file_path: str) -> Dict
```

#### Dataset Loader
- **Sample Policy Dataset**: GDPR, Executive Orders, EPA regulations
- **Government Websites**: Federal Register, EPA, CDC
- **CSV/SQL Integration**: Structured compliance data

#### Document Processing Pipeline
1. **Ingestion**: Upload/URL → Content extraction
2. **Preprocessing**: Text cleaning and normalization
3. **Vectorization**: Embedding generation (text-embedding-3-large)
4. **Indexing**: Vector storage and metadata tagging
5. **Retrieval**: Semantic search and ranking

### 3. Tool Integration Architecture

#### A. Marketplace Tools (aiXplain)
```python
tools = [
    ModelTool(model="6849dd3fd208307eba0cc122"),  # Document processor
    ModelTool(model="66f423426eb563fa213a3531"),  # Web scraper
    ModelTool(model="65c51c556eb563350f6e1bb1"),  # Google Search
    AgentFactory.create_python_interpreter_tool()  # Code interpreter
]
```

#### B. Custom Python Tools
```python
class PolicyStatusChecker:
    def check_policy_status(self, policy_id: str) -> Dict
    
class ComplianceAnalyzer:
    def analyze_compliance_requirements(self, business_type: str, size: str) -> Dict
    
class PolicySearchTool:
    def search_policies(self, query: str, source: str = "federal") -> List[Dict]
```

#### C. External API Integration
- **Federal Register API**: Real-time policy status
- **CourtListener API**: Case law retrieval
- **EPA Regulations API**: Environmental compliance
- **CDC Policy API**: Public health guidelines

#### D. Structured Data Tools
- **SQL Integration**: Compliance database queries
- **CSV Processing**: Structured policy data
- **Python Interpreter**: Dynamic analysis and calculations

### 4. External Tool Integration

#### Slack Integration
```python
class SlackIntegration:
    def send_policy_alert(self, policy_info: Dict) -> bool
    # Sends formatted policy updates to Slack channels
```

#### Notion Integration
```python
class NotionIntegration:
    def create_policy_page(self, policy_data: Dict) -> Dict
    # Creates policy tracking pages in Notion workspace
```

#### Calendar Integration
```python
class CalendarIntegration:
    def schedule_compliance_reminder(self, policy_name: str, deadline: str) -> Dict
    # Schedules compliance deadline reminders
```

## Data Flow

### 1. Query Processing Flow
```
User Query → Flask API → Policy Agent → Tool Selection → Data Retrieval → Response Generation → User Interface
```

### 2. Document Indexing Flow
```
Document/URL → Content Extraction → Text Processing → Vector Generation → Storage → Search Index Update
```

### 3. External Alert Flow
```
Policy Update → Agent Analysis → Alert Generation → External Tools (Slack/Notion/Calendar) → User Notification
```

## Technology Stack

### Backend
- **Framework**: Flask (API server)
- **AI Platform**: aiXplain SDK
- **Language Model**: GPT-4 via aiXplain
- **Vector Storage**: Custom implementation with semantic search
- **Data Processing**: pandas, BeautifulSoup, requests
- **External APIs**: Federal Register, CourtListener

### Frontend
- **Framework**: React 18
- **Styling**: Modern CSS with glassmorphism effects
- **HTTP Client**: Axios
- **Icons**: Lucide React
- **Build Tool**: Create React App

### Infrastructure
- **Environment**: Python 3.8+
- **Package Management**: pip, npm
- **Configuration**: Environment variables (.env)
- **Deployment**: Local development, cloud-ready

## Security Architecture

### API Security
- **Authentication**: TEAM_API_KEY validation
- **Input Validation**: Request sanitization and validation
- **Error Handling**: Secure error messages without sensitive data exposure
- **Rate Limiting**: Configurable request limits (future enhancement)

### Data Security
- **Sensitive Data**: No storage of sensitive government data
- **API Keys**: Environment variable storage only
- **External Integrations**: Optional webhook/token configuration
- **File Uploads**: Temporary file handling with cleanup

## Scalability Design

### Horizontal Scaling
- **Stateless Design**: No server-side session storage
- **API-First Architecture**: Microservices-ready design
- **External Tool Integration**: Distributed notification system
- **Cloud Deployment**: aiXplain cloud agent deployment

### Performance Optimization
- **Caching Strategy**: Vector search result caching (future)
- **Async Processing**: Background document indexing (future)
- **Load Balancing**: Multiple agent instances (future)
- **CDN Integration**: Static asset delivery (future)

## Monitoring and Logging

### System Monitoring
- **Health Checks**: `/api/health` endpoint
- **System Statistics**: `/api/stats` endpoint
- **Error Tracking**: Comprehensive exception handling
- **Performance Metrics**: Response time tracking

### Logging Strategy
```python
# Comprehensive logging throughout the system
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# API request logging
logger.info(f"Processing query: {query}")

# Error logging
logger.error(f"Failed to process query: {error}")

# Performance logging
logger.info(f"Query processed in {response_time}ms")
```

## Deployment Architecture

### Local Development
```bash
# Backend
python api_server.py  # Port 8000

# Frontend
cd frontend && npm start  # Port 3000

# Full Stack
python run_app.py  # Both servers
```

### Production Deployment (Future)
- **Backend**: Docker containerization
- **Frontend**: Static site deployment (Vercel/Netlify)
- **Database**: Vector database (Pinecone/Weaviate)
- **Monitoring**: Application performance monitoring
- **CI/CD**: Automated testing and deployment

## Extension Points

### Adding New Data Sources
1. Implement data loader in `src/data_processing/dataset_loader.py`
2. Add vector indexing logic
3. Update agent configuration
4. Test integration

### Adding New Tools
1. Create tool class in `src/tools/`
2. Register with agent factory
3. Add API endpoints if needed
4. Update documentation

### Adding New External Integrations
1. Implement integration class in `src/tools/external_integrations.py`
2. Add configuration variables
3. Update alert system
4. Test webhook/API integration

This architecture provides a robust, scalable foundation for the Policy Navigator system while maintaining flexibility for future enhancements and integrations.