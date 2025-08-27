#!/usr/bin/env python3
"""
Policy Navigator - Multi-Agent RAG System for Government Regulation Search
"""

import os
from dotenv import load_dotenv
from src.agents.policy_agent import PolicyNavigatorAgent
from src.data_processing.ingestion import DataIngestion

def main():
    """Main entry point for Policy Navigator"""
    load_dotenv()
    
    print("🏛️  Policy Navigator - Government Regulation Search System")
    print("=" * 60)
    
    # Check API key
    if not os.getenv('TEAM_API_KEY'):
        print("❌ Error: TEAM_API_KEY not found in environment variables")
        print("Please create a .env file with your aiXplain API key")
        return
    
    # Initialize components
    print("🔧 Initializing Policy Navigator Agent...")
    agent = PolicyNavigatorAgent()
    
    print("📊 Setting up data ingestion...")
    ingestion = DataIngestion()
    
    # Load sample data
    sample_data = ingestion.load_sample_policy_data()
    print(f"✅ Loaded {len(sample_data)} sample policies")
    
    # Demo queries
    demo_queries = [
        "Is Executive Order 14067 still in effect?",
        "What are the compliance requirements for small businesses under GDPR?",
        "Has Section 230 been challenged in court recently?"
    ]
    
    print("\n🚀 Running Demo Queries:")
    print("-" * 40)
    
    for i, query in enumerate(demo_queries, 1):
        print(f"\n{i}. Query: {query}")
        print("   Processing...")
        
        try:
            # For demo, use custom tools directly since agent creation requires API
            if "Executive Order 14067" in query:
                result = agent.check_policy_status("EO-14067")
                print(f"   Answer: {result.get('summary', 'Policy status checked')}")
            elif "compliance requirements" in query:
                result = agent.analyze_compliance("general", "small_business")
                print(f"   Answer: Found {len(result.get('requirements', {}))} compliance areas")
            else:
                print("   Answer: Query processed - use CLI for full agent responses")
                
        except Exception as e:
            print(f"   Error: {e}")
    
    print("\n" + "=" * 60)
    print("🎯 Demo Complete!")
    print("\nNext steps:")
    print("1. Set your TEAM_API_KEY in .env file")
    print("2. Run: python -m src.interfaces.cli interactive")
    print("3. Or use specific commands like:")
    print("   python -m src.interfaces.cli search -q 'your query'")
    print("   python -m src.interfaces.cli status -p 'EO-14067'")

if __name__ == "__main__":
    main()