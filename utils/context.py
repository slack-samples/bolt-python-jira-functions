import os
import secrets
from typing import Optional
from urllib.parse import urljoin

from jira.oauth.installation_store.file import JiraFileInstallationStore
from jira.oauth.installation_store.installation_store import JiraInstallationStore
from jira.oauth.state_store.file import JiraFileOAuthStateStore
from jira.oauth.state_store.state_store import JiraOAuthStateStore


class Context:
    def __init__(
        self,
        jira_base_url: Optional[str] = None,
        jira_client_id: Optional[str] = None,
        jira_client_secret: Optional[str] = None,
        jira_code_verifier: Optional[str] = None,
        app_base_url: Optional[str] = None,
        jira_oauth_redirect_path: str = "/oauth/redirect",
        app_home_page_url: Optional[str] = None,
        jira_state_store: JiraOAuthStateStore = JiraFileOAuthStateStore(),
        jira_installation_store: JiraInstallationStore = JiraFileInstallationStore(),
    ):
        self.jira_base_url = jira_base_url or os.getenv("JIRA_BASE_URL")
        self.jira_client_id = jira_client_id or os.getenv("JIRA_CLIENT_ID")
        self.jira_client_secret = jira_client_secret or os.getenv("JIRA_CLIENT_SECRET")
        self.app_base_url = app_base_url or os.getenv("APP_BASE_URL")
        self.app_home_page_url = app_home_page_url or os.getenv("APP_HOME_PAGE_URL")

        self.jira_code_verifier = jira_code_verifier or secrets.token_urlsafe(96)[:128]
        self.jira_oauth_redirect_path = jira_oauth_redirect_path
        self.jira_redirect_uri = urljoin(self.app_base_url, self.jira_oauth_redirect_path)

        self.jira_state_store = jira_state_store
        self.jira_installation_store = jira_installation_store
