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


class State(metaclass=Singleton):
    _users: Dict[str, str] = {}

    def create_user(self, username: str) -> None:
        self._users[username] = None

    def update_user(self, username: str) -> None:
        self._users[username] = None

    def read_user(self, username: str) -> str:
        return self._users[username]

    def delete_user(self, username: str) -> None:
        self._users.pop(username)
