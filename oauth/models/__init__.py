from typing import Optional


class UserIdentity:
    def __init__(self, user_id: str, team_id: Optional[str], enterprise_id: Optional[str]):
        self.user_id = user_id
        self.team_id = team_id
        self.enterprise_id = enterprise_id
