# Policy Navigator React Frontend

A modern React interface for the Policy Navigator system.

## Quick Start

### Option 1: Full Stack (Recommended)
```bash
# From project root
python run_app.py
```

### Option 2: Frontend Only
```bash
cd frontend
npm install
npm start
```

## Features

- **Policy Search**: Natural language queries for government regulations
- **Status Checker**: Real-time policy status verification  
- **Compliance Analysis**: Business compliance requirements analysis
- **Modern UI**: Clean, responsive interface with loading states

## API Endpoints

- `POST /api/query` - Search policies
- `POST /api/status` - Check policy status
- `POST /api/compliance` - Analyze compliance
- `GET /api/health` - Health check

## Usage

1. Enter your query in the search box
2. Choose action: Search, Status Check, or Compliance Analysis
3. View results in the results panel

The frontend automatically connects to the Flask API backend running on port 8000.