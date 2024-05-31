import json
import logging
import os
import uuid
from pathlib import Path
from typing import Optional, Union

from jira.oauth.state_store.state_store import JiraOAuthStateStore

from .models import JiraUserIdentity


class JiraFileOAuthStateStore(JiraOAuthStateStore):
    def __init__(
        self,
        *,
        base_dir: str = "./data/jira-oauth-state",
        logger: logging.Logger = logging.getLogger(__name__),
    ):
        self.base_dir = base_dir
        self.logger = logger

    def issue(self, user_identity: JiraUserIdentity) -> str:
        state = uuid.uuid4().hex
        self._mkdir(self.base_dir)
        filepath = f"{self.base_dir}/{state}"
        with open(filepath, "w") as f:
            content = json.dumps(user_identity)
            f.write(content)
        return state

    def consume(self, state: str) -> Optional[JiraUserIdentity]:
        filepath = f"{self.base_dir}/{state}"
        try:
            with open(filepath) as f:
                user_identity: JiraUserIdentity = json.load(f)

            os.remove(filepath)  # consume the file by deleting it
            return user_identity

        except FileNotFoundError as e:
            message = f"Failed to find any persistent data for state: {state} - {e}"
            self.logger.warning(message)
            return None

    @staticmethod
    def _mkdir(path: Union[str, Path]):
        if isinstance(path, str):
            path = Path(path)
        path.mkdir(parents=True, exist_ok=True)
