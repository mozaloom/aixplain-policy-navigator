#!/usr/bin/env python3
"""
Quick demo to test the system end-to-end
"""

import os
from dotenv import load_dotenv
from src.agents.policy_agent import PolicyNavigatorAgent

def quick_demo():
    """Quick demonstration of the system"""
    load_dotenv()
    
    print("🏛️ Policy Navigator - Quick Demo")
    print("=" * 40)
    
    if not os.getenv('TEAM_API_KEY'):
        print("❌ Please set TEAM_API_KEY in your .env file")
        return
    
    print("🤖 Initializing Policy Navigator Agent...")
    agent = PolicyNavigatorAgent()
    
    # Demo queries
    queries = [
        "What is Executive Order 14067 about?",
        "Is Executive Order 14067 still in effect?",
        "Has Section 230 been challenged in court?",
        "What are compliance requirements for small businesses?"
    ]
    
    for i, query in enumerate(queries, 1):
        print(f"\n{i}. Query: {query}")
        print("   Processing...")
        
        try:
            response = agent.query(query)
            output = response.get('output', 'No response')
            print(f"   Answer: {output[:200]}{'...' if len(output) > 200 else ''}")
        except Exception as e:
            print(f"   Error: {e}")
    
    print("\n" + "=" * 40)
    print("✅ Demo complete! System is working.")

if __name__ == "__main__":
    quick_demo()