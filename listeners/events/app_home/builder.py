from typing import TypedDict

from listeners.internals import CONNECT_ACCOUNT_ACTION, DISCONNECT_ACCOUNT_ACTION


class AppHome(TypedDict):
    type: str
    blocks: list


class AppHomeBuilder:
    def __init__(self):
        self.view: AppHome = {
            "type": "home",
            "blocks": [
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": "Welcome to the Jira Server App",
                    },
                },
                {"type": "divider"},
            ],
        }

    def add_connect_account_button(self, authorization_url):
        self.view["blocks"].append(
            {
                "type": "actions",
                "elements": [
                    {
                        "type": "button",
                        "text": {
                            "type": "plain_text",
                            "text": "Connect an Account",
                        },
                        "url": authorization_url,
                        "action_id": CONNECT_ACCOUNT_ACTION,
                    }
                ],
            }
        )

    def add_disconnect_account_button(self):
        self.view["blocks"].append(
            {
                "type": "actions",
                "elements": [
                    {
                        "type": "button",
                        "text": {
                            "type": "plain_text",
                            "text": "Disconnect Account",
                        },
                        "action_id": DISCONNECT_ACCOUNT_ACTION,
                    }
                ],
            }
        )
