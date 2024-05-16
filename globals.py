import os
from typing import Dict

from oauth.installation_store import FileInstallationStore
from oauth.models import UserIdentity

OAUTH_REDIRECT_PATH = "/oauth/redirect"
OAUTH_STATE_TABLE: Dict[str, UserIdentity] = {}
JIRA_FILE_INSTALLATION_STORE = FileInstallationStore(base_dir="./data/installations")

JIRA_BASE_URL = os.getenv("JIRA_BASE_URL")  # https://jira.atlassian.com
JIRA_CLIENT_ID = os.getenv("JIRA_CLIENT_ID")
JIRA_CLIENT_SECRET = os.getenv("JIRA_CLIENT_SECRET")
JIRA_CODE_VERIFIER = os.getenv("CODE_VERIFIER")
JIRA_REDIRECT_URI = os.getenv("APP_BASE_URL") + OAUTH_REDIRECT_PATH
APP_HOME_PAGE_URL = os.getenv("APP_HOME_PAGE_URL")
