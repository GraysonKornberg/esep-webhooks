import json
import os
import requests


def lambda_handler(event, context):
    
    try:
        issue = event.get("issue")
        
        # Extract the issue URL from the payload
        issue_url = issue["html_url"]
        
        # Prepare the message to send to Slack
        payload = {
            "text": f"Issue Created: {issue_url}"
        }
        
        # Get the Slack webhook URL from environment variables
        slack_url = os.getenv("SLACK_URL")
        
        if not slack_url:
            return {
                "statusCode": 500,
                "body": json.dumps({"error": "Slack URL not configured"})
            }
        
        # Send a POST request to the Slack webhook URL
        response = requests.post(slack_url, json=payload, headers={"Content-Type": "application/json"})
        
        
        # Return success response
        return {
            "statusCode": 200,
            "body": json.dumps({"message": "Notification sent to Slack"})
        }
    
    except KeyError:
        return {
            "statusCode": 400,
            "body": json.dumps({"error": "Invalid payload"})
        }
    
    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps({"error": "Internal server error"})
        }
