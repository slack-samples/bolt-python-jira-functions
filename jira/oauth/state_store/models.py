from typing import Optional, TypedDict


class JiraUserIdentity(TypedDict):
    """Class for keeping track of individual slack users"""

    user_id: str
    # Either team_id or enterprise_id must exist here
    team_id: Optional[str]
    enterprise_id: Optional[str]
