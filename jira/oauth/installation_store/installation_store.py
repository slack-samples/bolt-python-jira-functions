from typing import Optional

from .models import JiraInstallation


class JiraInstallationStore:
    def save(self, installation: JiraInstallation):
        """Saves an installation data"""
        raise NotImplementedError()

    def find_installation(
        self,
        *,
        enterprise_id: Optional[str],
        team_id: Optional[str],
        user_id: str,
    ) -> Optional[JiraInstallation]:
        """Finds a relevant installation for the given IDs."""
        raise NotImplementedError()

    def delete_installation(
        self,
        *,
        enterprise_id: Optional[str],
        team_id: Optional[str],
        user_id: str,
    ) -> None:
        """Deletes an installation that matches the given IDs"""
        raise NotImplementedError()
