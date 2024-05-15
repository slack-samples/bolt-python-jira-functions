import os
from typing import Union, Dict


class UserIdentity:
    def __init__(self, user_id: str, team_id: Union[str, None], enterprise_id: Union[str, None]):
        self.user_id = user_id
        self.team_id = team_id
        self.enterprise_id = enterprise_id


JIRA_BASE_URL = os.getenv("JIRA_BASE_URL")
OAUTH_REDIRECT_PATH = "/oauth/redirect"
JIRA_CLIENT_ID = os.getenv("JIRA_CLIENT_ID")
JIRA_CLIENT_SECRET = os.getenv("JIRA_CLIENT_SECRET")
JIRA_CODE_VERIFIER = os.getenv("CODE_VERIFIER")
JIRA_REDIRECT_URI = os.getenv("APP_BASE_URL") + OAUTH_REDIRECT_PATH
APP_HOME_PAGE_URL = os.getenv("APP_HOME_PAGE_URL")
OAUTH_STATE_TABLE: Dict[str, UserIdentity] = {}
