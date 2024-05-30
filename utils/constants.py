import secrets

OAUTH_REDIRECT_PATH = "/oauth/redirect"
JIRA_CODE_VERIFIER = secrets.token_urlsafe(96)[:128]
