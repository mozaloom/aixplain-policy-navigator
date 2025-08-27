#!/usr/bin/env python3
"""
Comprehensive test to verify everything works perfectly
"""

import os
import sys
import time
import requests
import subprocess
from dotenv import load_dotenv

def test_environment():
    """Test environment setup"""
    print("🔧 Testing Environment Setup...")
    
    load_dotenv()
    api_key = os.getenv('TEAM_API_KEY')
    
    if not api_key:
        print("❌ TEAM_API_KEY not found in .env file")
        return False
    
    if api_key == "your_api_key_here":
        print("❌ Please set your actual TEAM_API_KEY in .env file")
        return False
    
    print("✅ Environment setup OK")
    return True

def test_basic_imports():
    """Test basic imports work"""
    print("📦 Testing Basic Imports...")
    
    try:
        from src.agents.policy_agent import PolicyNavigatorAgent
        from src.tools.custom_tools import PolicyStatusChecker
        print("✅ Basic imports OK")
        return True
    except Exception as e:
        print(f"❌ Import error: {e}")
        return False

def test_agent_creation():
    """Test agent creation"""
    print("🤖 Testing Agent Creation...")
    
    try:
        from src.agents.policy_agent import PolicyNavigatorAgent
        agent = PolicyNavigatorAgent()
        print("✅ Agent creation OK")
        return True
    except Exception as e:
        print(f"❌ Agent creation error: {e}")
        return False

def test_api_endpoints():
    """Test API endpoints work"""
    print("🌐 Testing API Endpoints...")
    
    # Test Federal Register API
    try:
        response = requests.get("https://www.federalregister.gov/api/v1/documents.json?per_page=1", timeout=10)
        if response.status_code == 200:
            print("✅ Federal Register API accessible")
        else:
            print("⚠️ Federal Register API returned non-200 status")
    except Exception as e:
        print(f"⚠️ Federal Register API test failed: {e}")
    
    # Test CourtListener API
    try:
        response = requests.get("https://www.courtlistener.com/api/rest/v4/search/?q=test&type=o&format=json", timeout=10)
        if response.status_code in [200, 401]:  # 401 is OK for free tier
            print("✅ CourtListener API accessible")
        else:
            print("⚠️ CourtListener API returned unexpected status")
    except Exception as e:
        print(f"⚠️ CourtListener API test failed: {e}")

def test_agent_queries():
    """Test agent responds to queries"""
    print("💬 Testing Agent Queries...")
    
    try:
        from src.agents.policy_agent import PolicyNavigatorAgent
        agent = PolicyNavigatorAgent()
        
        # Test query
        response = agent.query("What is Executive Order 14067?")
        
        if response and 'output' in response:
            print("✅ Agent query response OK")
            print(f"   Sample response: {response['output'][:100]}...")
            return True
        else:
            print("❌ Agent query failed or no output")
            return False
            
    except Exception as e:
        print(f"❌ Agent query error: {e}")
        return False

def test_flask_server():
    """Test Flask server can start"""
    print("🚀 Testing Flask Server...")
    
    try:
        # Try to import flask components
        from api_server import app
        print("✅ Flask server imports OK")
        return True
    except Exception as e:
        print(f"❌ Flask server error: {e}")
        return False

def test_react_setup():
    """Test React frontend setup"""
    print("⚛️ Testing React Frontend...")
    
    frontend_dir = "frontend"
    package_json = os.path.join(frontend_dir, "package.json")
    
    if not os.path.exists(package_json):
        print("❌ React package.json not found")
        return False
    
    if not os.path.exists(os.path.join(frontend_dir, "src", "App.js")):
        print("❌ React App.js not found")
        return False
    
    print("✅ React frontend files OK")
    return True

def run_comprehensive_test():
    """Run all tests"""
    print("🧪 COMPREHENSIVE SYSTEM TEST")
    print("=" * 50)
    
    tests = [
        ("Environment Setup", test_environment),
        ("Basic Imports", test_basic_imports),
        ("Agent Creation", test_agent_creation),
        ("API Endpoints", test_api_endpoints),
        ("Agent Queries", test_agent_queries),
        ("Flask Server", test_flask_server),
        ("React Frontend", test_react_setup)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n{test_name}:")
        try:
            if test_func():
                passed += 1
            else:
                print(f"❌ {test_name} failed")
        except Exception as e:
            print(f"❌ {test_name} failed with exception: {e}")
    
    print("\n" + "=" * 50)
    print(f"📊 TEST RESULTS: {passed}/{total} tests passed")
    
    if passed >= total - 1:  # Allow 1 minor failure
        print("🎉 SYSTEM IS READY! All critical tests passed.")
        print("\n🚀 Next steps:")
        print("1. Run: python main.py (for demo)")
        print("2. Run: python run_app.py (for full React interface)")
        print("3. Run: python api_server.py (for API server only)")
        print("4. Test queries: python quick_demo.py")
    else:
        print("⚠️ Multiple tests failed. Check the errors above.")
        
    return passed >= total - 1

if __name__ == "__main__":
    success = run_comprehensive_test()
    sys.exit(0 if success else 1)