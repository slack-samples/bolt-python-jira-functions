from typing import Optional, TypedDict


class JiraUserIdentity(TypedDict):
    """Class for keeping track of individual slack users"""

    user_id: str
    team_id: Optional[str]
    enterprise_id: Optional[str]
