import os

from tests.mock_jira_installation_store import MockJiraInstallationStore
from tests.mock_jira_oauth_state_store import MockJiraOAuthStateStore
from utils.context import Context


def remove_os_env_temporarily() -> dict:
    old_env = os.environ.copy()
    os.environ.clear()
    return old_env


def restore_os_env(old_env: dict) -> None:
    os.environ.update(old_env)


def build_mock_context() -> Context:
    return Context(
        jira_base_url="https://jira-dev/",
        jira_client_id="abc123_id",
        jira_client_secret="abc123_secret",
        app_base_url="http://127.0.0.1:3000",
        app_home_page_url="slack://app?team=T123&id=A123&tab=home",
        jira_installation_store=MockJiraInstallationStore(),
        jira_state_store=MockJiraOAuthStateStore(),
    )
