from slack_bolt import Ack, BoltContext

from globals import JIRA_FILE_INSTALLATION_STORE


def disconnect_account_callback(ack: Ack, context: BoltContext):
    ack()
    JIRA_FILE_INSTALLATION_STORE.delete_installation(
        enterprise_id=context.enterprise_id, team_id=context.team_id, user_id=context.user_id
    )
