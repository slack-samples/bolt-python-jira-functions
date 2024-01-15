from slack_bolt import App

from .create_issue import create_issue_callback


def register(app: App):
    app.function("create_issue")(create_issue_callback)
