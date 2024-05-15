from logging import Logger
import uuid

from slack_sdk import WebClient
from slack_bolt import BoltContext
import urllib.parse

from controllers import AppHomeBuilder

from constants import JIRA_BASE_URL, JIRA_CLIENT_ID, JIRA_CODE_VERIFIER, JIRA_REDIRECT_URI, OAUTH_STATE_TABLE, UserIdentity


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
        params = {
            "client_id": JIRA_CLIENT_ID,
            "redirect_uri": JIRA_REDIRECT_URI,
            "response_type": "code",
            "scope": "WRITE",
            "code_challenge": JIRA_CODE_VERIFIER,
            "code_challenge_method": "plain",
            "state": state,
        }
        authorization_url = f"{JIRA_BASE_URL}/rest/oauth2/latest/authorize?{urllib.parse.urlencode(params)}"
        home.add_oauth_link_button(authorization_url)
        client.views_publish(user_id=context.user_id, view=home.view)
    except Exception as e:
        logger.error(f"Error publishing home tab: {e}")
