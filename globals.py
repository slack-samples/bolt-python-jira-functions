import os
import secrets
from urllib.parse import urljoin

OAUTH_REDIRECT_PATH = "/oauth/redirect"
JIRA_CODE_VERIFIER = secrets.token_urlsafe(96)[:128]

JIRA_BASE_URL = os.getenv("JIRA_BASE_URL")  # ex: https://jira.atlassian.com
JIRA_CLIENT_ID = os.getenv("JIRA_CLIENT_ID")
JIRA_CLIENT_SECRET = os.getenv("JIRA_CLIENT_SECRET")
JIRA_REDIRECT_URI = urljoin(os.getenv("APP_BASE_URL"), OAUTH_REDIRECT_PATH)
APP_HOME_PAGE_URL = os.getenv("APP_HOME_PAGE_URL")
