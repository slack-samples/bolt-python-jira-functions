from logging import Logger
import logging
from typing import Dict, Optional

from oauth.installation_store.installation_store import InstallationStore
from oauth.installation_store.models import JiraInstallation


class MockInstallationStore(InstallationStore):
    def __init__(
        self,
        *,
        logger: Logger = logging.getLogger(__name__),
    ):
        self.installation_table: Dict[str, JiraInstallation] = {}
        self.logger = logger

    def save(self, installation: JiraInstallation):
        installation_key = self._get_key(installation["enterprise_id"], installation["team_id"], installation["user_id"])
        self.installation_table[installation_key] = installation

    def find_installation(
        self,
        *,
        enterprise_id: Optional[str],
        team_id: Optional[str],
        user_id: str,
    ) -> Optional[JiraInstallation]:
        installation_key = self._get_key(enterprise_id, team_id, user_id)

        installation = self.installation_table.get(installation_key, None)
        if installation is None:
            message = f"Installation data missing for enterprise: {enterprise_id}, team: {team_id}: not found"
            self.logger.debug(message)
        return installation

    def delete_installation(
        self,
        *,
        enterprise_id: Optional[str],
        team_id: Optional[str],
        user_id: str,
    ) -> None:
        installation_key = self._get_key(enterprise_id, team_id, user_id)
        if installation_key in self.installation_table:
            del self.installation_table[installation_key]
        else:
            message = f"Failed to delete installation data for enterprise: {enterprise_id}, team: {team_id}: not found"
            self.logger.warning(message)

    def clear(self):
        self.installation_table.clear()

    def _get_key(self, enterprise_id: Optional[str], team_id: Optional[str], user_id: str):
        none = "none"
        e_id = enterprise_id or none
        t_id = team_id or none
        return f"{e_id}-{t_id}/installer-{user_id}-latest"
