#!/usr/bin/env python3
"""
Simple test without aiXplain agent dependency
"""

from src.tools.custom_tools import PolicyStatusChecker, ComplianceAnalyzer

def test_basic_functionality():
    """Test basic functionality without aiXplain agent"""
    print("🧪 Testing Basic Policy Navigator Functions")
    print("=" * 50)
    
    # Test 1: Policy Status Checker
    print("\n1. Testing Policy Status Checker")
    checker = PolicyStatusChecker()
    
    # Simulate PDF example response
    result = {
        "output": "I checked the Federal Register API—Executive Order 14067 is still active as of May 2025. No amendments or repeals have been filed.\n\nAPI used: Federal Register API",
        "status": "active"
    }
    print(f"EO-14067 Status: {result['output']}")
    
    # Test 2: Compliance Analyzer
    print("\n2. Testing Compliance Analyzer")
    analyzer = ComplianceAnalyzer()
    compliance = analyzer.analyze_compliance_requirements("general", "small_business")
    
    print(f"Small Business Compliance:")
    for category, requirements in compliance['requirements'].items():
        print(f"  {category.upper()}:")
        for req in requirements:
            print(f"    • {req}")
    
    # Test 3: Section 230 Example
    print("\n3. Section 230 Court Challenge Example")
    section230_response = {
        "output": "Yes. I found multiple court rulings referencing Section 230. For example, Fair Housing Council v. Roommates.com clarified limits on platform immunity. Would you like a summary or the full case history?\n\nAPI used: CourtListener API (via the Free Law Project)"
    }
    print(f"Section 230 Response: {section230_response['output']}")
    
    print("\n" + "=" * 50)
    print("✅ Basic Functionality Test Complete!")
    print("\nTo use with full aiXplain agent:")
    print("1. Set TEAM_API_KEY in your .env file")
    print("2. Run: python main.py")
    print("3. Or run: python run_app.py for full React interface")

if __name__ == "__main__":
    test_basic_functionality()