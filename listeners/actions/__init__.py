from slack_bolt import App

from .connect_account import connect_account_callback
from .disconnect_account import disconnect_account_callback


def register(app: App):
    app.action("connect_account")(connect_account_callback)
    app.action("disconnect_account")(disconnect_account_callback)
