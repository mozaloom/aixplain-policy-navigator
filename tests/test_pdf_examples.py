#!/usr/bin/env python3
"""
Test script to verify the system works exactly like PDF examples
"""

import os
from dotenv import load_dotenv
from src.agents.policy_agent import PolicyNavigatorAgent

def test_pdf_examples():
    """Test the exact examples from the PDF"""
    load_dotenv()
    
    print("🧪 Testing Policy Navigator - PDF Examples")
    print("=" * 50)
    
    agent = PolicyNavigatorAgent()
    
    # Test 1: Executive Order 14067 Status Check
    print("\n1. Testing Executive Order 14067 Status Check")
    print("User: 'Is Executive Order 14067 still in effect or has it been repealed?'")
    
    response1 = agent.query("Is Executive Order 14067 still in effect or has it been repealed?")
    print(f"Agent: {response1.get('output', 'No response')}")
    
    # Test 2: Section 230 Court Challenge
    print("\n2. Testing Section 230 Court Challenge")
    print("User: 'Has Section 230 ever been challenged in court? What was the outcome?'")
    
    response2 = agent.query("Has Section 230 ever been challenged in court? What was the outcome?")
    print(f"Agent: {response2.get('output', 'No response')}")
    
    # Test 3: Policy Status Check (Direct API)
    print("\n3. Testing Direct Policy Status Check")
    print("Checking EO-14067 status...")
    
    status_response = agent.check_policy_status("EO-14067")
    print(f"Status: {status_response.get('output', 'No response')}")
    
    # Test 4: Compliance Analysis
    print("\n4. Testing Compliance Analysis")
    print("Analyzing compliance for small business...")
    
    compliance_response = agent.analyze_compliance("general", "small_business")
    print(f"Compliance: {compliance_response.get('output', 'No response')}")
    
    print("\n" + "=" * 50)
    print("✅ PDF Examples Test Complete!")
    
    # Verify responses match PDF format
    expected_phrases = [
        "Federal Register API",
        "still active as of May 2025",
        "CourtListener API",
        "Fair Housing Council v. Roommates.com"
    ]
    
    all_responses = [
        response1.get('output', ''),
        response2.get('output', ''),
        status_response.get('output', ''),
        compliance_response.get('output', '')
    ]
    
    found_phrases = []
    for phrase in expected_phrases:
        for response in all_responses:
            if phrase in response:
                found_phrases.append(phrase)
                break
    
    print(f"\n📊 Verification: {len(found_phrases)}/{len(expected_phrases)} expected phrases found")
    for phrase in found_phrases:
        print(f"  ✅ Found: '{phrase}'")
    
    missing = set(expected_phrases) - set(found_phrases)
    for phrase in missing:
        print(f"  ❌ Missing: '{phrase}'")

if __name__ == "__main__":
    test_pdf_examples()