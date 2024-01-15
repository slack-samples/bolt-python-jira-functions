from logging import Logger

from slack_bolt import Ack
from slack_sdk import WebClient

from controllers import PersonalAccessTokenTable, AppHomeBuilder


def submit_pat_callback(ack: Ack, client: WebClient, body: dict, logger: Logger):
    try:
        ack()
        user_id = body["user"]["id"]

        home = AppHomeBuilder()
        home.add_clear_pat_button()
        client.views_publish(user_id=user_id, view=home.view)

        pat_table = PersonalAccessTokenTable()
        pat_table.create_user(
            user_id=user_id,
            personal_access_token=body["view"]["state"]["values"]["user_jira_pat_input"]["user_jira_pat"]["value"],
        )
    except Exception as e:
        logger.error(e)
