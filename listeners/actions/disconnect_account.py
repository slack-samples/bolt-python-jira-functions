from slack_bolt import Ack, BoltContext

from oauth.installation_store.file import FileInstallationStore


def disconnect_account_callback(ack: Ack, context: BoltContext):
    ack()
    FileInstallationStore().delete_installation(
        enterprise_id=context.enterprise_id, team_id=context.team_id, user_id=context.user_id
    )
