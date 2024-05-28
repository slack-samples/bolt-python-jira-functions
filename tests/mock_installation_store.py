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
        none = "none"
        e_id = installation["enterprise_id"] or none
        t_id = installation["team_id"] or none
        team_installation_dir = f"{e_id}-{t_id}"

        u_id = installation["user_id"]
        installer_filepath = f"{team_installation_dir}/installer-{u_id}-latest"
        self.installation_table[installer_filepath] = installation

    def find_installation(
        self,
        *,
        enterprise_id: Optional[str],
        team_id: Optional[str],
        user_id: str,
    ) -> Optional[JiraInstallation]:
        none = "none"
        e_id = enterprise_id or none
        t_id = team_id or none
        installation_filepath = f"{e_id}-{t_id}/installer-{user_id}-latest"

        installation = self.installation_table.get(installation_filepath, None)
        if installation is None:
            message = f"Installation data missing for enterprise: {e_id}, team: {t_id}: not found"
            self.logger.debug(message)
        return installation

    def delete_installation(
        self,
        *,
        enterprise_id: Optional[str],
        team_id: Optional[str],
        user_id: str,
    ) -> None:
        none = "none"
        e_id = enterprise_id or none
        t_id = team_id or none
        installation_filepath = f"{e_id}-{t_id}/installer-{user_id}-latest"
        if installation_filepath in self.installation_table:
            del self.installation_table[installation_filepath]
        else:
            message = f"Failed to delete installation data for enterprise: {e_id}, team: {t_id}: not found"
            self.logger.warning(message)

    def clear(self):
        self.installation_table.clear()
