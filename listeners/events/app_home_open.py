import uuid
from logging import Logger

from slack_bolt import BoltContext
from slack_sdk import WebClient

from controllers import AppHomeBuilder
from globals import JIRA_CLIENT_ID, JIRA_CODE_VERIFIER, JIRA_REDIRECT_URI, OAUTH_STATE_TABLE, UserIdentity
from jira.client import JiraClient


def app_home_open_callback(client: WebClient, event: dict, logger: Logger, context: BoltContext):
    # ignore the app_home_opened event for anything but the Home tab
    if event["tab"] != "home":
        return
    state = uuid.uuid4().hex
    OAUTH_STATE_TABLE[state] = UserIdentity(
        user_id=context.user_id, team_id=context.team_id, enterprise_id=context.enterprise_id
    )
    try:
        home = AppHomeBuilder()
        jira_client = JiraClient()
        authorization_url = jira_client.build_authorization_url(
            client_id=JIRA_CLIENT_ID,
            redirect_uri=JIRA_REDIRECT_URI,
            scope="WRITE",
            code_challenge=JIRA_CODE_VERIFIER,
            state=state,
        )
        home.add_oauth_link_button(authorization_url)
        client.views_publish(user_id=context.user_id, view=home.view)
    except Exception as e:
        logger.error(f"Error publishing home tab: {e}")
