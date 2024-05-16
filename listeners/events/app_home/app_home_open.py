import uuid
from logging import Logger

from slack_bolt import BoltContext
from slack_sdk import WebClient

from .builder import AppHomeBuilder
from globals import (
    JIRA_CLIENT_ID,
    JIRA_CODE_VERIFIER,
    JIRA_FILE_INSTALLATION_STORE,
    JIRA_REDIRECT_URI,
    OAUTH_STATE_TABLE,
    UserIdentity,
)
from jira.client import JiraClient


def app_home_open_callback(client: WebClient, event: dict, logger: Logger, context: BoltContext):
    # ignore the app_home_opened event for anything but the Home tab
    if event["tab"] != "home":
        return
    try:
        home = AppHomeBuilder()
        installation = JIRA_FILE_INSTALLATION_STORE.find_installation(
            user_id=context.user_id, team_id=context.team_id, enterprise_id=context.enterprise_id
        )

        if installation is None:
            state = uuid.uuid4().hex
            OAUTH_STATE_TABLE[state] = UserIdentity(
                user_id=context.user_id, team_id=context.team_id, enterprise_id=context.enterprise_id
            )
            jira_client = JiraClient()
            authorization_url = jira_client.build_authorization_url(
                client_id=JIRA_CLIENT_ID,
                redirect_uri=JIRA_REDIRECT_URI,
                scope="WRITE",
                code_challenge=JIRA_CODE_VERIFIER,
                state=state,
            )
            home.add_connect_account_button(authorization_url)
        else:
            home.add_disconnect_account_button()
        client.views_publish(user_id=context.user_id, view=home.view)
    except Exception as e:
        logger.error(f"Error publishing home tab: {e}")
