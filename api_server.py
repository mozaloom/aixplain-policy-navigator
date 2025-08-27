#!/usr/bin/env python3
"""
Flask API server for Policy Navigator React frontend
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from dotenv import load_dotenv
from src.agents.policy_agent import PolicyNavigatorAgent

load_dotenv()

app = Flask(__name__)
CORS(app)

# Initialize agent
agent = PolicyNavigatorAgent()

@app.route('/api/query', methods=['POST'])
def query_policies():
    """Handle policy queries - let agent decide what to do"""
    try:
        data = request.get_json()
        query = data.get('query', '')
        
        if not query:
            return jsonify({'error': 'Query is required'}), 400
        
        # Let the agent intelligently decide what APIs/tools to use
        result = agent.query(query)
        return jsonify(result)
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/status', methods=['POST'])
def check_status():
    """Check policy status"""
    try:
        data = request.get_json()
        policy_id = data.get('policy_id', '')
        
        if not policy_id:
            return jsonify({'error': 'Policy ID is required'}), 400
        
        result = agent.check_policy_status(policy_id)
        return jsonify(result)
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/compliance', methods=['POST'])
def analyze_compliance():
    """Analyze compliance requirements"""
    try:
        data = request.get_json()
        business_type = data.get('business_type', 'general')
        size = data.get('size', 'small_business')
        
        result = agent.analyze_compliance(business_type, size)
        return jsonify(result)
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({'status': 'healthy', 'service': 'Policy Navigator API'})

@app.route('/api/upload', methods=['POST'])
def upload_document():
    """Upload and index policy document"""
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file provided'}), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        # Save file temporarily
        file_path = f"temp_{file.filename}"
        file.save(file_path)
        
        # Index the document
        result = agent.upload_document(file_path)
        
        # Clean up
        os.remove(file_path)
        
        return jsonify(result)
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/index-url', methods=['POST'])
def index_url():
    """Index content from URL"""
    try:
        data = request.get_json()
        url = data.get('url', '')
        
        if not url:
            return jsonify({'error': 'URL is required'}), 400
        
        result = agent.index_url(url)
        return jsonify(result)
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/search-indexed', methods=['POST'])
def search_indexed():
    """Search indexed documents"""
    try:
        data = request.get_json()
        query = data.get('query', '')
        
        if not query:
            return jsonify({'error': 'Query is required'}), 400
        
        results = agent.search_indexed_content(query)
        return jsonify({'results': results})
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/stats', methods=['GET'])
def get_stats():
    """Get system statistics"""
    try:
        stats = agent.get_system_stats()
        return jsonify(stats)
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/send-alert', methods=['POST'])
def send_alert():
    """Send policy alert to external tools"""
    try:
        data = request.get_json()
        policy_info = data.get('policy_info', {})
        
        result = agent.send_policy_alert(policy_info)
        return jsonify(result)
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8000))
    app.run(host='0.0.0.0', port=port, debug=True)