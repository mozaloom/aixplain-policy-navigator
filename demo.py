#!/usr/bin/env python3
"""
Policy Navigator Demo Script
Demonstrates the Multi-Agent RAG System capabilities
"""

import os
import time
from dotenv import load_dotenv
from src.agents.policy_agent import PolicyNavigatorAgent
from src.data_processing.ingestion import DataIngestion
from src.tools.federal_register_api import FederalRegisterAPI
from src.tools.court_listener_api import CourtListenerAPI

def print_header(title):
    """Print formatted header"""
    print("\n" + "="*60)
    print(f"🎯 {title}")
    print("="*60)

def print_section(title):
    """Print formatted section"""
    print(f"\n📋 {title}")
    print("-"*40)

def simulate_typing(text, delay=0.03):
    """Simulate typing effect"""
    for char in text:
        print(char, end='', flush=True)
        time.sleep(delay)
    print()

def demo_data_ingestion():
    """Demonstrate data ingestion capabilities"""
    print_section("Data Ingestion Demo")
    
    ingestion = DataIngestion()
    
    print("🔄 Loading sample policy data...")
    sample_data = ingestion.load_sample_policy_data()
    print(f"✅ Loaded {len(sample_data)} sample policies")
    
    print("\n📊 Sample policies:")
    for _, policy in sample_data.iterrows():
        print(f"  • {policy['policy_id']}: {policy['title']}")
    
    print("\n🌐 Scraping Federal Register (limited demo)...")
    fed_docs = ingestion.scrape_federal_register(limit=5)
    print(f"✅ Retrieved {len(fed_docs)} recent documents")

def demo_api_integrations():
    """Demonstrate API integrations"""
    print_section("API Integration Demo")
    
    # Federal Register API
    print("🏛️ Federal Register API Demo:")
    fed_api = FederalRegisterAPI()
    
    print("  Searching for 'digital assets'...")
    docs = fed_api.search_documents("digital assets", limit=3)
    
    if docs:
        print(f"  ✅ Found {len(docs)} documents:")
        for doc in docs[:2]:
            print(f"    • {doc.get('title', 'No title')[:60]}...")
    else:
        print("  ⚠️  No documents found (API may be rate limited)")
    
    # CourtListener API
    print("\n⚖️ CourtListener API Demo:")
    court_api = CourtListenerAPI()
    
    print("  Searching for 'Section 230'...")
    cases = court_api.search_opinions("Section 230", limit=2)
    
    if cases:
        print(f"  ✅ Found {len(cases)} cases:")
        for case in cases[:1]:
            print(f"    • {case.get('caseName', 'Unknown case')}")
    else:
        print("  ⚠️  No cases found (API may require authentication)")

def demo_policy_queries():
    """Demonstrate policy query capabilities"""
    print_section("Policy Query Demo")
    
    agent = PolicyNavigatorAgent()
    
    # Demo queries with simulated responses
    queries = [
        {
            "query": "Is Executive Order 14067 still in effect?",
            "response": "Executive Order 14067 (Ensuring Responsible Development of Digital Assets) is still active. Published on March 9, 2022, it remains in effect with no amendments or repeals filed."
        },
        {
            "query": "What are the compliance requirements for small businesses under GDPR?",
            "response": "Small businesses under GDPR have simplified requirements: no mandatory DPO, simplified reporting, but must still ensure data protection by design and conduct annual compliance reviews."
        },
        {
            "query": "Has Section 230 been challenged in court recently?",
            "response": "Recent Section 230 challenges include Gonzalez v. Google (2023) and Twitter v. Taamneh (2023). The law remains largely intact with narrow exceptions."
        }
    ]
    
    for i, item in enumerate(queries, 1):
        print(f"\n{i}. Query: {item['query']}")
        print("   🤖 Agent processing...")
        
        # Simulate processing time
        time.sleep(1)
        
        # Try actual agent query if API key is available
        if os.getenv('AIXPLAIN_API_KEY'):
            try:
                # Use custom tools for demo
                if "Executive Order 14067" in item['query']:
                    result = agent.check_policy_status("EO-14067")
                    response = result.get('summary', item['response'])
                elif "compliance requirements" in item['query']:
                    result = agent.analyze_compliance("general", "small_business")
                    response = f"Found {len(result.get('requirements', {}))} compliance areas for small businesses"
                else:
                    response = item['response']
            except Exception as e:
                response = f"Demo response: {item['response']}"
        else:
            response = f"Demo response: {item['response']}"
        
        print(f"   💡 Answer: {response}")

def demo_compliance_analysis():
    """Demonstrate compliance analysis"""
    print_section("Compliance Analysis Demo")
    
    agent = PolicyNavigatorAgent()
    
    business_types = [
        ("small_business", "Small Business"),
        ("large_business", "Large Enterprise")
    ]
    
    for size, label in business_types:
        print(f"\n📊 {label} Compliance Analysis:")
        
        analysis = agent.analyze_compliance("tech_company", size)
        
        print(f"   Business Size: {analysis['size']}")
        print("   Key Requirements:")
        
        for regulation, requirements in analysis['requirements'].items():
            print(f"     {regulation.upper()}:")
            for req in requirements[:2]:  # Show first 2 requirements
                print(f"       • {req}")
        
        print("   Deadlines:")
        for deadline in analysis['deadlines'][:2]:
            print(f"     • {deadline}")

def demo_status_checking():
    """Demonstrate policy status checking"""
    print_section("Policy Status Checking Demo")
    
    agent = PolicyNavigatorAgent()
    
    policies = ["EO-14067", "GDPR", "Section-230"]
    
    for policy_id in policies:
        print(f"\n🔍 Checking status for: {policy_id}")
        
        try:
            status = agent.check_policy_status(policy_id)
            federal_status = status.get('federal_status', {})
            
            print(f"   Status: {federal_status.get('status', 'Unknown')}")
            if 'title' in federal_status:
                print(f"   Title: {federal_status['title'][:50]}...")
            if 'publication_date' in federal_status:
                print(f"   Date: {federal_status['publication_date']}")
            
        except Exception as e:
            print(f"   ⚠️  Error checking status: {e}")

def main():
    """Run the complete demo"""
    load_dotenv()
    
    print_header("Policy Navigator - Multi-Agent RAG System Demo")
    
    print("🚀 Welcome to the Policy Navigator demonstration!")
    print("This demo showcases a Multi-Agent RAG system for government regulation search.")
    
    if not os.getenv('AIXPLAIN_API_KEY'):
        print("\n⚠️  Note: AIXPLAIN_API_KEY not found - running in demo mode")
        print("Set your API key in .env for full functionality")
    else:
        print("\n✅ aiXplain API key detected - full functionality available")
    
    # Run demo sections
    demo_data_ingestion()
    demo_api_integrations()
    demo_policy_queries()
    demo_compliance_analysis()
    demo_status_checking()
    
    print_header("Demo Complete!")
    
    print("🎉 Policy Navigator Demo finished successfully!")
    print("\n📚 What you've seen:")
    print("  ✅ Multi-agent RAG architecture with aiXplain SDK")
    print("  ✅ Integration with Federal Register and CourtListener APIs")
    print("  ✅ Policy status checking and compliance analysis")
    print("  ✅ Natural language query processing")
    print("  ✅ Real-time data ingestion from government sources")
    
    print("\n🚀 Next Steps:")
    print("  1. Set up your AIXPLAIN_API_KEY in .env")
    print("  2. Run: python -m src.interfaces.cli interactive")
    print("  3. Try queries like:")
    print("     • 'Is Executive Order 14067 still active?'")
    print("     • 'What are GDPR requirements for startups?'")
    print("     • 'Show me recent EPA regulations'")
    
    print("\n📖 Full documentation: README.md")
    print("🔧 CLI help: python -m src.interfaces.cli --help")

if __name__ == "__main__":
    main()