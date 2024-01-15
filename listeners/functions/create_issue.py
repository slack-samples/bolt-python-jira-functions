import logging
import os

from slack_bolt import Complete, Fail, Say, Ack
import requests
from controllers import PersonalAccessTokenTable
import json

JIRA_BASE_URL = os.getenv("JIRA_BASE_URL")


# https://developer.atlassian.com/server/jira/platform/jira-rest-api-examples/
# https://developer.atlassian.com/cloud/jira/platform/rest/v2/api-group-issues/#api-rest-api-2-issue-post
def create_issue_callback(ack: Ack, inputs: dict, fail: Fail, complete: Complete, logger: logging.Logger):
    ack()
    pat_table = PersonalAccessTokenTable()

    user_id = inputs["user_id"]

    if user_id not in pat_table:
        # TODO send a message to user on how to fix this
        return fail(f"User {user_id} has not set up their PAT properly, visit the app home to do this")

    try:
        project: str = inputs["project"]
        issue_type = inputs["issuetype"]
        # assignee = inputs["assignee"]
        summary = inputs["summary"]
        description = inputs["description"]

        url = f"{JIRA_BASE_URL}/rest/api/2/issue"

        headers = {
            "Authorization": f"Bearer {pat_table.read_pat(user_id)}",
            "Accept": "application/json",
            "Content-Type": "application/json",
        }

        payload = json.dumps(
            {
                "fields": {
                    "description": description,
                    "issuetype": {"id" if issue_type.isdigit() else "name": issue_type},
                    "labels": ["bugfix", "blitz_test"],
                    "project": {"id" if project.isdigit() else "key": project},
                    "summary": summary,
                },
            }
        )

        # response = requests.request("POST", url, data=payload, headers=headers)

        # logger.info(json.loads(response.text))
        complete(outputs={"issue_url": "https://media.giphy.com/media/NEvPzZ8bd1V4Y/giphy.gif"})
    except Exception as e:
        logger.exception(e)
        fail(f"Failed to handle a function request (error: {e})")
