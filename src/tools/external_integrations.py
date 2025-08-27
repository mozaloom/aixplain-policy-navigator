import os
import json
import requests
from datetime import datetime, timedelta
from typing import Dict, List, Optional

class SlackIntegration:
    def __init__(self, webhook_url: Optional[str] = None):
        self.webhook_url = webhook_url or os.getenv('SLACK_WEBHOOK_URL')
    
    def send_policy_alert(self, policy_info: Dict) -> bool:
        """Send policy update to Slack"""
        if not self.webhook_url:
            print("Slack webhook not configured")
            return False
        
        message = {
            "text": f"🏛️ Policy Update Alert",
            "blocks": [
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": f"*Policy:* {policy_info.get('title', 'Unknown')}\n*Status:* {policy_info.get('status', 'Unknown')}\n*Source:* {policy_info.get('source', 'Federal Register')}"
                    }
                }
            ]
        }
        
        try:
            print(f"Sending to webhook: {self.webhook_url[:50]}...")
            print(f"Message: {message}")
            
            response = requests.post(self.webhook_url, json=message)
            
            print(f"Response status: {response.status_code}")
            print(f"Response text: {response.text}")
            
            return response.status_code == 200
        except Exception as e:
            print(f"Slack notification failed: {e}")
            return False

class CalendarIntegration:
    def __init__(self):
        self.reminders = []
    
    def schedule_compliance_reminder(self, policy_name: str, deadline: str) -> Dict:
        """Schedule compliance deadline reminder"""
        reminder = {
            "id": len(self.reminders) + 1,
            "policy": policy_name,
            "deadline": deadline,
            "created": datetime.now().isoformat(),
            "type": "compliance_deadline"
        }
        
        self.reminders.append(reminder)
        
        return {
            "success": True,
            "message": f"Reminder scheduled for {policy_name} deadline: {deadline}",
            "reminder_id": reminder["id"]
        }
    
    def get_upcoming_reminders(self, days: int = 30) -> List[Dict]:
        """Get upcoming compliance reminders"""
        return [r for r in self.reminders if r["type"] == "compliance_deadline"]

class NotionIntegration:
    def __init__(self, token: Optional[str] = None):
        self.token = token or os.getenv('NOTION_TOKEN')
        self.headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json",
            "Notion-Version": "2022-06-28"
        } if self.token else {}
    
    def create_policy_page(self, policy_data: Dict) -> Dict:
        """Create a policy tracking page in Notion"""
        if not self.token:
            # Simulate Notion page creation
            return {
                "success": True,
                "message": f"Policy page created for {policy_data.get('title', 'Unknown Policy')}",
                "page_id": f"notion_page_{len(policy_data.get('title', ''))}"
            }
        
        # Real Notion API implementation would go here
        return {"success": False, "message": "Notion integration not fully configured"}

class ExternalToolManager:
    def __init__(self):
        self.slack = SlackIntegration()
        self.calendar = CalendarIntegration()
        self.notion = NotionIntegration()
    
    def handle_policy_update(self, policy_info: Dict) -> Dict:
        """Handle policy updates across all external tools"""
        results = {}
        
        # Send Slack notification
        results['slack'] = self.slack.send_policy_alert(policy_info)
        
        # Create Notion page
        results['notion'] = self.notion.create_policy_page(policy_info)
        
        # Schedule reminder if deadline exists
        if policy_info.get('deadline'):
            results['calendar'] = self.calendar.schedule_compliance_reminder(
                policy_info.get('title', 'Policy'),
                policy_info.get('deadline')
            )
        
        return results