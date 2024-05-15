from slack_bolt import Ack


def oauth_url_callback(ack: Ack):
    ack()
