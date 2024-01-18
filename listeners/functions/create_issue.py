import logging
import os
import sys

from slack_bolt import Complete, Fail, Ack
import requests
from controllers import PersonalAccessTokenTable
import json


# https://developer.atlassian.com/server/jira/platform/jira-rest-api-examples/
# https://developer.atlassian.com/cloud/jira/platform/rest/v2/api-group-issues/#api-rest-api-2-issue-post
def create_issue_callback(
    ack: Ack, inputs: dict, fail: Fail, complete: Complete, logger: logging.Logger, pat_table=PersonalAccessTokenTable()
):
    ack()
    JIRA_BASE_URL = os.getenv("JIRA_BASE_URL")

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

        url = f"{JIRA_BASE_URL}rest/api/2/issue"

        headers = {
            "Authorization": f"Bearer {pat_table.read_pat(user_id)}",
            "Accept": "application/json;charset=UTF-8",
            "Content-Type": "application/json;charset=UTF-8",
        }

        payload = json.dumps(
            {
                "fields": {
                    "description": description,
                    "issuetype": {"id" if issue_type.isdigit() else "name": issue_type},
                    "project": {"id" if project.isdigit() else "key": project},
                    "summary": summary,
                },
            }
        )

        print(payload)

        response = requests.get(
            url,
            data=payload,
            headers=headers,
        )

        logger.info(response)

        print(response.status_code)
        for k, v in response.headers.items():
            print(f"{k}: {v}")
        # logger.info(response.json())
        logger.info(response.text)
        jason_data = json.loads(response.text)
        logger.info(jason_data)
        complete(outputs={"issue_url": jason_data["self"]})
    except Exception as e:
        logger.exception(e)
        fail(f"Failed to handle a function request (error: {e})")
