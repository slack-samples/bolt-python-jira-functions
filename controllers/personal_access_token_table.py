class PersonalAccessTokenTable(dict):
    def __new__(cls):
        if not hasattr(cls, "instance"):
            cls.instance = super(PersonalAccessTokenTable, cls).__new__(cls)
        return cls.instance

    def create_user(self, user_id: str, personal_access_token: str) -> None:
        self[user_id] = personal_access_token

    def read_pat(self, user_id: str) -> str:
        return self[user_id]

    def delete_user(self, user_id: str) -> None:
        self.pop(user_id, None)
