# Policy Navigator API Documentation

## Overview

The Policy Navigator API provides RESTful endpoints for interacting with the multi-agent RAG system for government regulation search and compliance analysis.

## Base URL
```
http://localhost:8000/api
```

## Authentication
All requests require a valid `TEAM_API_KEY` in the environment variables.

## Endpoints

### 1. Query Policies
**POST** `/query`

Query the Policy Navigator agent with natural language.

**Request Body:**
```json
{
  "query": "Is Executive Order 14067 still in effect?"
}
```

**Response:**
```json
{
  "output": "I checked the Federal Register API—Executive Order 14067 is still active as of May 2025. No amendments or repeals have been filed.\n\nAPI used: Federal Register API"
}
```

### 2. Check Policy Status
**POST** `/status`

Check the status of a specific policy.

**Request Body:**
```json
{
  "policy_id": "EO-14067"
}
```

**Response:**
```json
{
  "output": "I checked the Federal Register API—Executive Order 14067 is still active as of May 2025. No amendments or repeals have been filed.\n\nAPI used: Federal Register API",
  "status": "active",
  "source": "Federal Register API"
}
```

### 3. Compliance Analysis
**POST** `/compliance`

Analyze compliance requirements for different business types.

**Request Body:**
```json
{
  "business_type": "tech_company",
  "size": "small_business"
}
```

**Response:**
```json
{
  "output": "Based on current regulations for small_business tech_company:\n\n• Data protection officer not required\n• Simplified reporting\n• Website accessibility required\n\nCompliance deadlines: Annual review required, Quarterly assessments\n\nSource: Government Compliance Database",
  "requirements": {
    "gdpr": ["Data protection officer not required", "Simplified reporting"],
    "ada": ["Website accessibility required"]
  },
  "deadlines": ["Annual review required", "Quarterly assessments"]
}
```

### 4. Upload Document
**POST** `/upload`

Upload and index a policy document.

**Request:**
- Content-Type: `multipart/form-data`
- File field: `file`

**Response:**
```json
{
  "status": "uploaded",
  "doc_id": "doc_123",
  "filename": "policy.pdf"
}
```

### 5. Index URL
**POST** `/index-url`

Index content from a government/regulatory URL.

**Request Body:**
```json
{
  "url": "https://www.epa.gov/laws-regulations"
}
```

**Response:**
```json
{
  "status": "indexed",
  "doc_id": "doc_124",
  "url": "https://www.epa.gov/laws-regulations",
  "title": "EPA Laws & Regulations"
}
```

### 6. Search Indexed Content
**POST** `/search-indexed`

Search through indexed documents.

**Request Body:**
```json
{
  "query": "environmental compliance"
}
```

**Response:**
```json
{
  "results": [
    {
      "doc_id": "doc_124",
      "content": "Environmental compliance requirements...",
      "metadata": {
        "source": "url",
        "title": "EPA Laws & Regulations"
      },
      "score": 5
    }
  ]
}
```

### 7. Send Alert
**POST** `/send-alert`

Send policy alert to external tools (Slack, Notion, Calendar).

**Request Body:**
```json
{
  "policy_info": {
    "title": "Executive Order 14067 Update",
    "status": "active",
    "deadline": "2025-12-31",
    "source": "Federal Register API"
  }
}
```

**Response:**
```json
{
  "slack": true,
  "notion": {
    "success": true,
    "message": "Policy page created for Executive Order 14067 Update",
    "page_id": "notion_page_123"
  },
  "calendar": {
    "success": true,
    "message": "Reminder scheduled for Executive Order 14067 Update deadline: 2025-12-31",
    "reminder_id": 1
  }
}
```

### 8. System Statistics
**GET** `/stats`

Get comprehensive system statistics.

**Response:**
```json
{
  "vector_store": {
    "total_documents": 6,
    "sources": {
      "sample_dataset": 3,
      "url": 3
    },
    "indexed_urls": 3
  },
  "datasets": [
    "sample_policy_dataset",
    "government_websites"
  ],
  "agent_status": "active"
}
```

### 9. Health Check
**GET** `/health`

Check API health status.

**Response:**
```json
{
  "status": "healthy",
  "service": "Policy Navigator API"
}
```

## Error Responses

All endpoints return appropriate HTTP status codes and error messages:

**400 Bad Request:**
```json
{
  "error": "Query is required"
}
```

**500 Internal Server Error:**
```json
{
  "error": "Failed to process query: Connection timeout"
}
```

## Rate Limits

- No rate limits currently implemented
- Recommended: 100 requests per minute per API key

## Examples

### cURL Examples

**Query Policy:**
```bash
curl -X POST http://localhost:8000/api/query \
  -H "Content-Type: application/json" \
  -d '{"query": "Is Executive Order 14067 still in effect?"}'
```

**Upload Document:**
```bash
curl -X POST http://localhost:8000/api/upload \
  -F "file=@policy.pdf"
```

**Check System Stats:**
```bash
curl http://localhost:8000/api/stats
```

### Python Examples

```python
import requests

# Query the agent
response = requests.post('http://localhost:8000/api/query', 
                        json={'query': 'What is Executive Order 14067?'})
print(response.json()['output'])

# Upload document
with open('policy.pdf', 'rb') as f:
    response = requests.post('http://localhost:8000/api/upload', 
                           files={'file': f})
print(response.json())

# Get system statistics
response = requests.get('http://localhost:8000/api/stats')
print(response.json())
```

### JavaScript Examples

```javascript
// Query the agent
const response = await fetch('http://localhost:8000/api/query', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ query: 'Has Section 230 been challenged in court?' })
});
const data = await response.json();
console.log(data.output);

// Send policy alert
const alertResponse = await fetch('http://localhost:8000/api/send-alert', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    policy_info: {
      title: 'Policy Update',
      status: 'active',
      deadline: '2025-12-31'
    }
  })
});
```

## Integration Guide

### React Frontend Integration
The React frontend automatically connects to these API endpoints via the proxy configuration in `package.json`.

### External Tool Integration
Configure external tools by setting environment variables:
```bash
SLACK_WEBHOOK_URL=https://hooks.slack.com/services/YOUR/SLACK/WEBHOOK
NOTION_TOKEN=your_notion_integration_token
```

### Error Handling
Always implement proper error handling:
```python
try:
    response = requests.post(url, json=data)
    response.raise_for_status()
    return response.json()
except requests.exceptions.RequestException as e:
    print(f"API request failed: {e}")
```