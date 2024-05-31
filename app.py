import logging
import os
from datetime import datetime

from flask import Flask, make_response, redirect, request
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler

from jira.client import JiraClient
from listeners import register_listeners
from utils.constants import CONTEXT

logging.basicConfig(level=logging.INFO)

app = App(token=os.environ.get("SLACK_BOT_TOKEN"))
flask_app = Flask(__name__)

# Register Listeners
register_listeners(app)


@flask_app.route(CONTEXT.jira_oauth_redirect_path, methods=["GET"])
def oauth_redirect():
    code = request.args["code"]
    state = request.args["state"]

    jira_client = JiraClient()
    jira_resp = jira_client.oauth2_token(
        code=code,
        client_id=CONTEXT.jira_client_id,
        client_secret=CONTEXT.jira_client_secret,
        code_verifier=CONTEXT.jira_code_verifier,
        redirect_uri=CONTEXT.jira_redirect_uri,
    )
    jira_resp.raise_for_status()
    jira_resp_json = jira_resp.json()

    user_identity = CONTEXT.jira_state_store.consume(state)

    if user_identity is None:
        return make_response("State Not Found", 404)

    CONTEXT.jira_installation_store.save(
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
    return redirect(CONTEXT.app_home_page_url, code=302)


if __name__ == "__main__":
    SocketModeHandler(app, os.environ.get("SLACK_APP_TOKEN")).connect()
    flask_app.run(port=3000)
