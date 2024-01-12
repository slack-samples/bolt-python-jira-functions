import logging

from slack_bolt import Complete, Fail, Say


def create_issue_callback(inputs: dict, say: Say, fail: Fail, complete: Complete, logger: logging.Logger):
    user_id = inputs["user_id"]

    try:
        say(
            channel=user_id,  # sending a DM to this user
            text="Click button to complete function!",
            blocks=[
                {
                    "type": "section",
                    "text": {"type": "mrkdwn", "text": "Click button to complete function!"},
                }
            ],
        )
        complete({"user_id": user_id})
    except Exception as e:
        logger.exception(e)
        fail(f"Failed to handle a function request (error: {e})")
