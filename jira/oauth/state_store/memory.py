import uuid
from typing import Dict

from .models import JiraUserIdentity

OAUTH_STATE_TABLE: Dict[str, JiraUserIdentity] = {}


class JiraMemoryOAuthStateStore:
    @staticmethod
    def issue(user_identity: JiraUserIdentity) -> str:
        state = uuid.uuid4().hex
        OAUTH_STATE_TABLE[state] = user_identity
        return state

    @staticmethod
    def consume(state: str) -> JiraUserIdentity:
        return OAUTH_STATE_TABLE.pop(state)
