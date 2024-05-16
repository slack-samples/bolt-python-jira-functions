from typing import TypedDict

context = "<https://confluence.atlassian.com/enterprise/using-personal-access-tokens-1026032365.html|Personal access tokens>\
(PATs) are a secure way to use scripts and integrate external applications with your Atlassian application. To use the\
functions defined by this app you will need to add your own, click the add button to submit yours."


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

    def add_oauth_link_button(self, authorization_url):
        self.view["blocks"].append(
            {
                "type": "actions",
                "elements": [
                    {
                        "type": "button",
                        "text": {
                            "type": "plain_text",
                            "text": "Link Jira",
                        },
                        "url": authorization_url,
                        "action_id": "oauth_url",
                    }
                ],
            }
        )

    def add_pat_submit_button(self):
        self.view["blocks"].append(
            {
                "type": "actions",
                "elements": [
                    {
                        "type": "button",
                        "text": {
                            "type": "plain_text",
                            "text": "Submit",
                        },
                        "action_id": "submit_pat",
                    }
                ],
            }
        )

    def add_pat_input_field(self):
        self.view["blocks"].append(
            {
                "type": "input",
                "block_id": "user_jira_pat_input",
                "element": {
                    "type": "plain_text_input",
                    "action_id": "user_jira_pat",
                    "placeholder": {"type": "plain_text", "text": "Enter your personal access token"},
                },
                "label": {"type": "plain_text", "text": "PAT"},
            }
        )

    def add_clear_pat_button(self):
        self.view["blocks"].append(
            {
                "type": "actions",
                "elements": [
                    {
                        "type": "button",
                        "text": {
                            "type": "plain_text",
                            "text": "Clear PAT",
                        },
                        "action_id": "clear_pat",
                    }
                ],
            }
        )
