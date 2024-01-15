from typing import Dict


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        """
        Possible changes to the value of the `__init__` argument do not affect
        the returned instance.
        """
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]


class PersonalAccessTokenTable(metaclass=Singleton):
    _users: Dict[str, str] = {}

    def create_user(self, user_id: str, personal_access_token: str) -> None:
        self._users[user_id] = personal_access_token

    def read_user(self, user_id: str) -> str:
        return self._users[user_id]

    def delete_user(self, user_id: str) -> None:
        self._users.pop(user_id, None)

    def __contains__(self, user_id: str) -> bool:
        return user_id in self._users
