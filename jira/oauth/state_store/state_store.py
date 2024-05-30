from .models import JiraUserIdentity


class JiraOAuthStateStore:
    def issue(user_identity: JiraUserIdentity) -> str:
        """Issues relevant state given an Identity"""
        raise NotImplementedError()

    def consume(state: str) -> JiraUserIdentity:
        """Consums a given state returns corresponding Identity"""
        raise NotImplementedError()
