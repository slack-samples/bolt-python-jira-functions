import logging
import os
from flask import Flask, request, redirect
import requests

from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler

from constants import (
    OAUTH_REDIRECT_PATH,
    JIRA_BASE_URL,
    JIRA_CLIENT_ID,
    JIRA_CLIENT_SECRET,
    JIRA_CODE_VERIFIER,
    JIRA_REDIRECT_URI,
    APP_HOME_PAGE_URL,
    OAUTH_STATE_TABLE,
)
from listeners import register_listeners

logging.basicConfig(level=logging.INFO)

app = App(token=os.environ.get("SLACK_BOT_TOKEN"))
flask_app = Flask(__name__)

# Register Listeners
register_listeners(app)


class JiraInstallation:
    def __init__(self, scope: str, access_token: str, token_type: str, expires_in: int, refresh_token: str):
        self.scope = scope
        self.access_token = access_token
        self.token_type = token_type
        self.expires_in = expires_in
        self.refresh_token = refresh_token


@flask_app.route(OAUTH_REDIRECT_PATH, methods=["GET"])
def oauth_redirect():
    code = request.args["code"]
    state = request.args["state"]
    headers = {"Content-Type": "application/x-www-form-urlencoded", "TSAuth-Token": os.getenv("HEADER_TSAuth_Token")}
    resp = requests.post(
        url=f"{JIRA_BASE_URL}/rest/oauth2/latest/token",
        params={
            "grant_type": "authorization_code",
            "client_id": JIRA_CLIENT_ID,
            "client_secret": JIRA_CLIENT_SECRET,
            "code": code,
            "redirect_uri": JIRA_REDIRECT_URI,
            "code_verifier": JIRA_CODE_VERIFIER,
        },
        headers=headers,
    )
    resp.raise_for_status()
    json = resp.json()
    jira_installation = JiraInstallation(
        scope=json["scope"],
        access_token=json["access_token"],
        token_type=json["token_type"],
        expires_in=json["expires_in"],
        refresh_token=json["refresh_token"],
    )
    print(jira_installation.access_token)
    user_indentity = OAUTH_STATE_TABLE[state]
    print(user_indentity.user_id)
    print(user_indentity.enterprise_id)
    print(user_indentity.team_id)
    del OAUTH_STATE_TABLE[state]
    return redirect(APP_HOME_PAGE_URL, code=302)


if __name__ == "__main__":
    SocketModeHandler(app, os.environ.get("SLACK_APP_TOKEN")).connect()
    flask_app.run(port=3000)
