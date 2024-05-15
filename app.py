import logging
import os
from flask import Flask, request, redirect
import requests

from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler

from listeners import register_listeners

logging.basicConfig(level=logging.INFO)

app = App(token=os.environ.get("SLACK_BOT_TOKEN"))
flask_app = Flask(__name__)

JIRA_BASE_URL = os.getenv("JIRA_BASE_URL")
oauth_redirect_path = "/oauth/redirect"
jira_client_id = os.getenv("JIRA_CLIENT_ID")
jira_client_secret = os.getenv("JIRA_CLIENT_SECRET")
jira_code_verifier = os.getenv("CODE_VERIFIER")
jira_redirect_uri = os.getenv("APP_BASE_URL") + oauth_redirect_path
app_home_page_url = os.getenv("APP_HOME_PAGE_URL")

# Register Listeners
register_listeners(app)

flask_app = Flask(__name__)

# params = {
#     "client_id": jira_client_id,
#     "redirect_uri": jira_redirect_uri,
#     "response_type": "code",
#     "scope": "WRITE",
#     "code_challenge": jira_code_verifier,
#     "code_challenge_method": "plain",
# }
# authorization_url = f"{JIRA_BASE_URL}/rest/oauth2/latest/authorize?{urllib.parse.urlencode(params)}"


class JiraInstallation:
    def __init__(self, scope: str, access_token: str, token_type: str, expires_in: int, refresh_token: str):
        self.scope = scope
        self.access_token = access_token
        self.token_type = token_type
        self.expires_in = expires_in
        self.refresh_token = refresh_token


# print(f"Please go to {authorization_url} and authorize access.")


@flask_app.route("/oauth/redirect", methods=["GET"])
def oauth_redirect():
    print(request.args)
    headers = {"Content-Type": "application/x-www-form-urlencoded", "TSAuth-Token": os.getenv("HEADER_TSAuth_Token")}
    resp = requests.post(
        url=f"{JIRA_BASE_URL}/rest/oauth2/latest/token",
        params={
            "grant_type": "authorization_code",
            "client_id": jira_client_id,
            "client_secret": jira_client_secret,
            "code": request.args["code"],
            "redirect_uri": jira_redirect_uri,
            "code_verifier": jira_code_verifier,
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
    print(jira_installation)
    return redirect(app_home_page_url, code=302)


if __name__ == "__main__":
    SocketModeHandler(app, os.environ.get("SLACK_APP_TOKEN")).connect()
    flask_app.run(port=3000)
