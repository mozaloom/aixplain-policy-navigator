#!/usr/bin/env python3
"""
Test Slack webhook integration
"""

import os
from dotenv import load_dotenv
from src.tools.external_integrations import SlackIntegration

def test_slack():
    """Test Slack webhook"""
    load_dotenv()
    
    webhook_url = os.getenv('SLACK_WEBHOOK_URL')
    
    if not webhook_url:
        print("❌ SLACK_WEBHOOK_URL not found in .env file")
        print("Please add your Slack webhook URL to .env file")
        return
    
    print("🔗 Testing Slack Integration...")
    
    slack = SlackIntegration(webhook_url)
    
    # Test policy alert
    policy_info = {
        "title": "Executive Order 14067 - Test Alert",
        "status": "Active",
        "source": "Federal Register API",
        "url": "https://www.federalregister.gov/documents/2022/03/14/2022-05471"
    }
    
    success = slack.send_policy_alert(policy_info)
    
    if success:
        print("✅ Slack notification sent successfully!")
        print("Check your Slack channel for the policy alert.")
    else:
        print("❌ Failed to send Slack notification")
        print("Check your webhook URL and try again")

if __name__ == "__main__":
    test_slack()