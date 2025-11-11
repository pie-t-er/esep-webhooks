import json
import os
import urllib.request

def lambda_handler(event, context):
    body = event.get("body")
    if body:
        try:
            payload = json.loads(body)
        except Exception:
            print("Body is not valid JSON, using raw string")
            payload = {"body": body}
    else:
        payload = event

    # Extract issue info
    try:
        issue_url = payload["issue"]["html_url"]
    except KeyError:
        print("No 'issue.html_url' in payload — check input structure")
        return {"statusCode": 400, "body": json.dumps({"error": "Missing issue data"})}

    # Build Slack message payload
    slack_message = {"text": f"Issue Created: {issue_url}"}

    # Read Slack webhook URL from environment variable
    slack_url = os.environ.get("SLACK_URL")
    if not slack_url:
        return {"statusCode": 500, "body": json.dumps({"error": "Missing SLACK_URL env var"})}

    # Send POST request to Slack
    data = json.dumps(slack_message).encode("utf-8")
    req = urllib.request.Request(slack_url, data=data, headers={"Content-Type": "application/json"})

    return {
        "statusCode": 200,
        "body": json.dumps({"message": "Slack notification sent successfully!"})
    }
