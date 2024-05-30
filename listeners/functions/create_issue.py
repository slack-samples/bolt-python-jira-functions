import json
import logging

from slack_bolt import Ack, BoltContext, Complete, Fail
from slack_sdk import WebClient

from jira.client import JiraClient
from utils.constants import CONTEXT


# https://developer.atlassian.com/server/jira/platform/jira-rest-api-examples/
# https://developer.atlassian.com/cloud/jira/platform/rest/v2/api-group-issues/#api-rest-api-2-issue-post
def create_issue_callback(
    ack: Ack, inputs: dict, fail: Fail, complete: Complete, context: BoltContext, client: WebClient, logger: logging.Logger
):
    ack()
    user_id = inputs["user_context"]["id"]

    installation = CONTEXT.jira_installation_store.find_installation(
        user_id=user_id, team_id=context.team_id, enterprise_id=context.enterprise_id
    )
    if installation is None:
        mrkdwn: str = (
            ":no_entry: There is a problem with the `Create an issue` step, you did not connect a Jira Account, "
            f"visit the <{CONTEXT.app_home_page_url}|App Home Page> to fix this!"
        )
        client.chat_postMessage(
            channel=user_id,
            text=mrkdwn,
            blocks=[
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": mrkdwn,
                    },
                }
            ],
        )
        return fail(
            f"User {user_id} has not connected their account properly, they must visit the App Home Page to fix this"
        )

    try:
        project: str = inputs["project"]
        issue_type: str = inputs["issuetype"]

        jira_client = JiraClient(token=installation["access_token"])
        response = jira_client.create_issue(
            data={
                "fields": {
                    "description": inputs["description"],
                    "issuetype": {"id" if issue_type.isdigit() else "name": issue_type},
                    "project": {"id" if project.isdigit() else "key": project},
                    "summary": inputs["summary"],
                },
            }
        )

        response.raise_for_status()
        jason_data = json.loads(response.text)
        complete(
            outputs={
                "issue_url": jira_client.build_issue_url(key=jason_data["key"]),
            }
        )
    except Exception as e:
        logger.exception(e)
        fail(f"Failed to handle a function request (error: {e})")
