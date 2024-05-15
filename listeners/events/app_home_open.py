from logging import Logger
import os

from slack_sdk import WebClient
import urllib.parse

from controllers import AppHomeBuilder

JIRA_BASE_URL = os.getenv("JIRA_BASE_URL")
oauth_redirect_path = "/oauth/redirect"
jira_client_id = os.getenv("JIRA_CLIENT_ID")
jira_client_secret = os.getenv("JIRA_CLIENT_SECRET")
jira_code_verifier = os.getenv("CODE_VERIFIER")
jira_redirect_uri = os.getenv("APP_BASE_URL") + oauth_redirect_path


def app_home_open_callback(client: WebClient, event: dict, logger: Logger):
    # ignore the app_home_opened event for anything but the Home tab
    if event["tab"] != "home":
        return
    user_id = event["user"]
    try:
        home = AppHomeBuilder()
        params = {
            "client_id": jira_client_id,
            "redirect_uri": jira_redirect_uri,
            "response_type": "code",
            "scope": "WRITE",
            "code_challenge": jira_code_verifier,
            "code_challenge_method": "plain",
        }
        authorization_url = f"{JIRA_BASE_URL}/rest/oauth2/latest/authorize?{urllib.parse.urlencode(params)}"
        home.add_oauth_link_button(authorization_url)
        client.views_publish(user_id=user_id, view=home.view)
    except Exception as e:
        logger.error(f"Error publishing home tab: {e}")
