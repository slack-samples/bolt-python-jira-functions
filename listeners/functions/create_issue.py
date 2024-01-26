import logging
import os

from slack_bolt import Complete, Fail, Ack
import requests
from controllers import PersonalAccessTokenTable
import json


# https://developer.atlassian.com/server/jira/platform/jira-rest-api-examples/
# https://developer.atlassian.com/cloud/jira/platform/rest/v2/api-group-issues/#api-rest-api-2-issue-post
def create_issue_callback(ack: Ack, inputs: dict, fail: Fail, complete: Complete, logger: logging.Logger):
    ack()
    pat_table = PersonalAccessTokenTable()

    user_id = inputs["user_id"]
    if user_id not in pat_table:
        # TODO send a message to user on how to fix this
        return fail(f"User {user_id} has not set up their PAT properly, visit the app home to do this")

    JIRA_BASE_URL = os.getenv("JIRA_BASE_URL")

    headers = {
        "Authorization": f"Bearer {pat_table.read_pat(user_id)}",
        "Accept": "application/json",
        "Content-Type": "application/json",
    }

    for name, value in os.environ.items():
        if name.startswith("HEADER_"):
            headers[name.split("HEADER_")[1].replace("_", "-")] = value

    try:
        project: str = inputs["project"]
        issue_type: str = inputs["issuetype"]

        url = f"{JIRA_BASE_URL}/rest/api/latest/issue"

        payload = json.dumps(
            {
                "fields": {
                    "description": inputs["description"],
                    "issuetype": {"id" if issue_type.isdigit() else "name": issue_type},
                    "project": {"id" if project.isdigit() else "key": project},
                    "summary": inputs["summary"],
                },
            }
        )

        response = requests.post(url, data=payload, headers=headers)

        jason_data = json.loads(response.text)
        complete(outputs={"issue_url": jason_data["self"]})
    except Exception as e:
        logger.exception(e)
        fail(f"Failed to handle a function request (error: {e})")
