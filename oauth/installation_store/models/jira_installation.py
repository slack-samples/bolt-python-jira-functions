from typing import Optional, TypedDict


class JiraInstallation(TypedDict):
    scope: str
    access_token: str
    token_type: str
    expires_in: int
    refresh_token: str
    user_id: str
    team_id: Optional[str]
    enterprise_id: Optional[str]
    installed_at: float
