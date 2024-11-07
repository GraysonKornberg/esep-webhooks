import json
import os
import logging
import requests

# Set up logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, context):
    # Log the received event for debugging purposes
    logger.info(f"Received event: {event}")
    
    try:
        # Parse the JSON body from the event (GitHub sends the payload in the "body" field)
        body = json.loads(event.get("body", "{}"))
        
        # Extract the issue URL from the payload
        issue_url = body["issue"]["html_url"]
        
        # Prepare the message to send to Slack
        payload = {
            "text": f"Issue Created: {issue_url}"
        }
        
        # Get the Slack webhook URL from environment variables
        slack_url = os.getenv("SLACK_URL")
        
        if not slack_url:
            logger.error("Slack URL not found in environment variables")
            return {
                "statusCode": 500,
                "body": json.dumps({"error": "Slack URL not configured"})
            }
        
        # Send a POST request to the Slack webhook URL
        response = requests.post(slack_url, json=payload, headers={"Content-Type": "application/json"})
        
        # Log the response from Slack
        logger.info(f"Slack response: {response.text}")
        
        # Return success response
        return {
            "statusCode": 200,
            "body": json.dumps({"message": "Notification sent to Slack"})
        }
    
    except KeyError:
        logger.error("Error parsing payload, 'issue' or 'html_url' key not found")
        return {
            "statusCode": 400,
            "body": json.dumps({"error": "Invalid payload"})
        }
    
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        return {
            "statusCode": 500,
            "body": json.dumps({"error": "Internal server error"})
        }
