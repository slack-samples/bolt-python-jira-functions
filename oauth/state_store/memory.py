import uuid
from typing import Dict

from .models import UserIdentity

OAUTH_STATE_TABLE: Dict[str, UserIdentity] = {}


class MemoryOAuthStateStore:
    @staticmethod
    def issue(user_identity: UserIdentity) -> str:
        state = uuid.uuid4().hex
        OAUTH_STATE_TABLE[state] = user_identity
        return state

    @staticmethod
    def consume(state: str) -> UserIdentity:
        return OAUTH_STATE_TABLE.pop(state)
