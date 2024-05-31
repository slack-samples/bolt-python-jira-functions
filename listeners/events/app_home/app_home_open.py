from logging import Logger

from slack_bolt import BoltContext
from slack_sdk import WebClient

from jira.client import JiraClient
from jira.oauth.state_store.models import JiraUserIdentity
from utils.constants import CONTEXT

from .builder import AppHomeBuilder


def app_home_open_callback(client: WebClient, event: dict, logger: Logger, context: BoltContext):
    # ignore the app_home_opened event for anything but the Home tab
    if event["tab"] != "home":
        return
    try:
        home = AppHomeBuilder()
        installation = CONTEXT.jira_installation_store.find_installation(
            user_id=context.user_id, team_id=context.team_id, enterprise_id=context.enterprise_id
        )

        if installation is None:
            state = CONTEXT.jira_state_store.issue(
                user_identity=JiraUserIdentity(
                    user_id=context.user_id, team_id=context.team_id, enterprise_id=context.enterprise_id
                )
            )
            jira_client = JiraClient()
            authorization_url = jira_client.build_authorization_url(
                client_id=CONTEXT.jira_client_id,
                redirect_uri=CONTEXT.jira_redirect_uri,
                scope="WRITE",
                code_challenge=CONTEXT.jira_code_verifier,
                state=state,
            )
            home.add_connect_account_button(authorization_url)
        else:
            home.add_disconnect_account_button()
        client.views_publish(user_id=context.user_id, view=home.view)
    except Exception as e:
        logger.error(f"Error publishing home tab: {e}")
