import json
import logging

from slack_bolt import Ack, BoltContext, Complete, Fail

from jira.client import JiraClient
from oauth.installation_store.file import FileInstallationStore


# https://developer.atlassian.com/server/jira/platform/jira-rest-api-examples/
# https://developer.atlassian.com/cloud/jira/platform/rest/v2/api-group-issues/#api-rest-api-2-issue-post
def create_issue_callback(
    ack: Ack, inputs: dict, fail: Fail, complete: Complete, logger: logging.Logger, context: BoltContext
):
    ack()
    user_id = inputs["user_context"]["id"]

    installation = FileInstallationStore().find_installation(
        user_id=user_id, team_id=context.team_id, enterprise_id=context.enterprise_id
    )
    if installation is None:
        return fail(f"User {user_id} has not connected their account properly, visit the app home to solve this")

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
        complete(outputs={"issue_url": jason_data["self"]})
    except Exception as e:
        logger.exception(e)
        fail(f"Failed to handle a function request (error: {e})")
