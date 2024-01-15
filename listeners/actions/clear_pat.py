from logging import Logger

from slack_bolt import Ack
from slack_sdk import WebClient

from controllers import PersonalAccessTokenTable, AppHomeBuilder


def clear_pat_callback(ack: Ack, client: WebClient, body: dict, logger: Logger):
    try:
        ack()
        user_id = body["user"]["id"]

        pat_table = PersonalAccessTokenTable()
        pat_table.delete_user(user_id=user_id)

        home = AppHomeBuilder()
        home.add_pat_input_field()
        home.add_pat_submit_button()
        client.views_publish(user_id=user_id, view=home.view)
    except Exception as e:
        logger.error(e)
