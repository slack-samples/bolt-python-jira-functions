from slack_bolt import Ack, BoltContext

from jira.oauth.installation_store.file import JiraFileInstallationStore


def disconnect_account_callback(ack: Ack, context: BoltContext):
    ack()
    JiraFileInstallationStore().delete_installation(
        enterprise_id=context.enterprise_id, team_id=context.team_id, user_id=context.user_id
    )
