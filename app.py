import logging
import os
from datetime import datetime

from flask import Flask, redirect, request
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler

from internals import (
    APP_HOME_PAGE_URL,
    JIRA_CLIENT_ID,
    JIRA_CLIENT_SECRET,
    JIRA_CODE_VERIFIER,
    JIRA_REDIRECT_URI,
    OAUTH_REDIRECT_PATH,
)
from jira.client import JiraClient
from jira.oauth.installation_store.file import JiraFileInstallationStore
from jira.oauth.state_store.memory import JiraMemoryOAuthStateStore
from listeners import register_listeners

logging.basicConfig(level=logging.INFO)

app = App(token=os.environ.get("SLACK_BOT_TOKEN"))
flask_app = Flask(__name__)

# Register Listeners
register_listeners(app)


@flask_app.route(OAUTH_REDIRECT_PATH, methods=["GET"])
def oauth_redirect():
    code = request.args["code"]
    state = request.args["state"]

    jira_client = JiraClient()
    jira_resp = jira_client.oauth2_token(
        code=code,
        client_id=JIRA_CLIENT_ID,
        client_secret=JIRA_CLIENT_SECRET,
        code_verifier=JIRA_CODE_VERIFIER,
        redirect_uri=JIRA_REDIRECT_URI,
    )
    jira_resp.raise_for_status()
    jira_resp_json = jira_resp.json()

    user_identity = JiraMemoryOAuthStateStore.consume(state)

    JiraFileInstallationStore().save(
        {
            "access_token": jira_resp_json["access_token"],
            "enterprise_id": user_identity["enterprise_id"],
            "expires_in": jira_resp_json["expires_in"],
            "installed_at": datetime.now().timestamp(),
            "refresh_token": jira_resp_json["refresh_token"],
            "scope": jira_resp_json["scope"],
            "team_id": user_identity["team_id"],
            "token_type": jira_resp_json["token_type"],
            "user_id": user_identity["user_id"],
        }
    )
    return redirect(APP_HOME_PAGE_URL, code=302)


if __name__ == "__main__":
    SocketModeHandler(app, os.environ.get("SLACK_APP_TOKEN")).connect()
    flask_app.run(port=3000)
