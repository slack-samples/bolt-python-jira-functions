import logging
import uuid
from logging import Logger
from typing import Dict, Optional

from jira.oauth.state_store.models import JiraUserIdentity
from jira.oauth.state_store.state_store import JiraOAuthStateStore


class MockJiraOAuthStateStore(JiraOAuthStateStore):
    def __init__(
        self,
        *,
        logger: Logger = logging.getLogger(__name__),
    ):
        self.state_table: Dict[str, JiraUserIdentity] = {}
        self.logger = logger

    def issue(self, user_identity: JiraUserIdentity) -> str:
        state = uuid.uuid4().hex
        self.state_table[state] = user_identity
        return state

    def consume(self, state: str) -> Optional[JiraUserIdentity]:
        if state not in self.state_table:
            message = f"Failed to find any persistent data for state: {state} - Key Error"
            self.logger.warning(message)
        return self.state_table.pop(state, None)
