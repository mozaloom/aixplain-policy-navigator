#!/usr/bin/env python3
"""
Test script for Policy Navigator system
Verifies all components work correctly
"""

import os
import sys
import traceback
from dotenv import load_dotenv

def test_imports():
    """Test that all modules can be imported"""
    print("🧪 Testing imports...")
    
    try:
        from src.agents.policy_agent import PolicyNavigatorAgent
        from src.data_processing.ingestion import DataIngestion
        from src.tools.federal_register_api import FederalRegisterAPI
        from src.tools.court_listener_api import CourtListenerAPI
        from src.tools.custom_tools import PolicyStatusChecker, ComplianceAnalyzer
        from src.utils.config import CONFIG
        print("✅ All imports successful")
        return True
    except Exception as e:
        print(f"❌ Import error: {e}")
        traceback.print_exc()
        return False

def test_configuration():
    """Test configuration loading"""
    print("\n🧪 Testing configuration...")
    
    try:
        from src.utils.config import CONFIG
        
        # Check required config sections
        required_sections = ['aixplain', 'data_sources', 'vector_store', 'tools']
        for section in required_sections:
            if section not in CONFIG:
                print(f"❌ Missing config section: {section}")
                return False
        
        print("✅ Configuration loaded successfully")
        return True
    except Exception as e:
        print(f"❌ Configuration error: {e}")
        return False

def test_data_ingestion():
    """Test data ingestion functionality"""
    print("\n🧪 Testing data ingestion...")
    
    try:
        from src.data_processing.ingestion import DataIngestion
        
        ingestion = DataIngestion()
        
        # Test sample data loading
        sample_data = ingestion.load_sample_policy_data()
        if len(sample_data) == 0:
            print("❌ No sample data loaded")
            return False
        
        print(f"✅ Loaded {len(sample_data)} sample policies")
        return True
    except Exception as e:
        print(f"❌ Data ingestion error: {e}")
        return False

def test_api_tools():
    """Test API integration tools"""
    print("\n🧪 Testing API tools...")
    
    try:
        from src.tools.federal_register_api import FederalRegisterAPI
        from src.tools.court_listener_api import CourtListenerAPI
        
        # Test Federal Register API
        fed_api = FederalRegisterAPI()
        print("✅ Federal Register API initialized")
        
        # Test CourtListener API
        court_api = CourtListenerAPI()
        print("✅ CourtListener API initialized")
        
        return True
    except Exception as e:
        print(f"❌ API tools error: {e}")
        return False

def test_custom_tools():
    """Test custom analysis tools"""
    print("\n🧪 Testing custom tools...")
    
    try:
        from src.tools.custom_tools import PolicyStatusChecker, ComplianceAnalyzer
        
        # Test policy status checker
        checker = PolicyStatusChecker()
        status = checker.check_policy_status("EO-14067")
        
        if 'policy_id' not in status:
            print("❌ Policy status checker failed")
            return False
        
        print("✅ Policy status checker working")
        
        # Test compliance analyzer
        analyzer = ComplianceAnalyzer()
        analysis = analyzer.analyze_compliance_requirements("tech", "small_business")
        
        if 'requirements' not in analysis:
            print("❌ Compliance analyzer failed")
            return False
        
        print("✅ Compliance analyzer working")
        return True
    except Exception as e:
        print(f"❌ Custom tools error: {e}")
        return False

def test_agent_creation():
    """Test agent creation (without API key)"""
    print("\n🧪 Testing agent creation...")
    
    try:
        from src.agents.policy_agent import PolicyNavigatorAgent
        
        agent = PolicyNavigatorAgent()
        
        # Test tool initialization
        if not hasattr(agent, 'policy_checker'):
            print("❌ Policy checker not initialized")
            return False
        
        if not hasattr(agent, 'compliance_analyzer'):
            print("❌ Compliance analyzer not initialized")
            return False
        
        print("✅ Agent components initialized")
        
        # Test custom methods (without creating aiXplain agent)
        status = agent.check_policy_status("test")
        compliance = agent.analyze_compliance("test", "small_business")
        
        print("✅ Agent methods working")
        return True
    except Exception as e:
        print(f"❌ Agent creation error: {e}")
        return False

def test_cli_imports():
    """Test CLI module imports"""
    print("\n🧪 Testing CLI imports...")
    
    try:
        from src.interfaces.cli import cli
        print("✅ CLI module imported successfully")
        return True
    except Exception as e:
        print(f"❌ CLI import error: {e}")
        return False

def test_file_structure():
    """Test that required files exist"""
    print("\n🧪 Testing file structure...")
    
    required_files = [
        'requirements.txt',
        'config/config.yaml',
        '.env.example',
        'src/agents/policy_agent.py',
        'src/tools/federal_register_api.py',
        'src/interfaces/cli.py',
        'main.py',
        'demo.py'
    ]
    
    missing_files = []
    for file_path in required_files:
        if not os.path.exists(file_path):
            missing_files.append(file_path)
    
    if missing_files:
        print(f"❌ Missing files: {missing_files}")
        return False
    
    print("✅ All required files present")
    return True

def main():
    """Run all tests"""
    load_dotenv()
    
    print("🧪 Policy Navigator System Tests")
    print("="*50)
    
    tests = [
        test_file_structure,
        test_imports,
        test_configuration,
        test_data_ingestion,
        test_api_tools,
        test_custom_tools,
        test_agent_creation,
        test_cli_imports
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        try:
            if test():
                passed += 1
        except Exception as e:
            print(f"❌ Test {test.__name__} failed with exception: {e}")
    
    print("\n" + "="*50)
    print(f"🎯 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! System is ready to use.")
        print("\n📋 Next steps:")
        print("1. Set AIXPLAIN_API_KEY in .env file")
        print("2. Run: python demo.py")
        print("3. Try: python -m src.interfaces.cli interactive")
    else:
        print("⚠️  Some tests failed. Please check the errors above.")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())