from logging import Logger

from slack_sdk import WebClient

from controllers import AppHomeBuilder, PersonalAccessTokenTable


def app_home_open_callback(client: WebClient, event: dict, logger: Logger):
    # ignore the app_home_opened event for anything but the Home tab
    if event["tab"] != "home":
        return
    try:
        home = AppHomeBuilder()
        pat_table = PersonalAccessTokenTable()
        if event["user"] in pat_table:
            home.add_clear_pat_button()
        else:
            home.add_pat_input_field()
            home.add_pat_submit_button()
        client.views_publish(user_id=event["user"], view=home.view)
    except Exception as e:
        logger.error(f"Error publishing home tab: {e}")
