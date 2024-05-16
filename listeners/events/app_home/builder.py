from typing import TypedDict

context = "Welcome to jira"


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
                        "text": context,
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
                        "action_id": "connect_account",
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
                        "action_id": "disconnect_account",
                    }
                ],
            }
        )
