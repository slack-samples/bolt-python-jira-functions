from slack_bolt import Ack, BoltContext

from utils.constants import CONTEXT


def disconnect_account_callback(ack: Ack, context: BoltContext):
    ack()
    CONTEXT.jira_installation_store.delete_installation(
        enterprise_id=context.enterprise_id, team_id=context.team_id, user_id=context.user_id
    )
