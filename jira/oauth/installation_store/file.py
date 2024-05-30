import glob
import json
import logging
import os
from logging import Logger
from pathlib import Path
from typing import Optional, Union

from jira.oauth.installation_store.installation_store import JiraInstallationStore
from jira.oauth.installation_store.models import JiraInstallation


class JiraFileInstallationStore(JiraInstallationStore):
    def __init__(
        self,
        *,
        base_dir: str = "./data/jira-installations",
        logger: Logger = logging.getLogger(__name__),
    ):
        self.base_dir = base_dir
        self.logger = logger

    def save(self, installation: JiraInstallation):
        none = "none"
        e_id = installation["enterprise_id"] or none
        t_id = installation["team_id"] or none
        team_installation_dir = f"{self.base_dir}/{e_id}-{t_id}"
        self._mkdir(team_installation_dir)

        u_id = installation["user_id"]
        installer_filepath = f"{team_installation_dir}/installer-{u_id}-latest"
        with open(installer_filepath, "w") as f:
            entity: str = json.dumps(installation)
            f.write(entity)

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
        installation_filepath = f"{self.base_dir}/{e_id}-{t_id}/installer-{user_id}-latest"

        try:
            installation: Optional[JiraInstallation] = None
            with open(installation_filepath) as f:
                data = json.loads(f.read())
                installation: JiraInstallation = data

            return installation

        except FileNotFoundError as e:
            message = f"Installation data missing for enterprise: {e_id}, team: {t_id}: {e}"
            self.logger.debug(message)
            return None

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
        filepath_glob = f"{self.base_dir}/{e_id}-{t_id}/installer-{user_id}-*"
        for filepath in glob.glob(filepath_glob):
            try:
                os.remove(filepath)
            except FileNotFoundError as e:
                message = f"Failed to delete installation data for enterprise: {e_id}, team: {t_id}: {e}"
                self.logger.warning(message)

    @staticmethod
    def _mkdir(path: Union[str, Path]):
        if isinstance(path, str):
            path = Path(path)
        path.mkdir(parents=True, exist_ok=True)
