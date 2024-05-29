from slack_bolt import App

from listeners.internals import CONNECT_ACCOUNT_ACTION, DISCONNECT_ACCOUNT_ACTION

from .disconnect_account import disconnect_account_callback


def register(app: App):
    app.action(CONNECT_ACCOUNT_ACTION)(lambda ack: ack())
    app.action(DISCONNECT_ACCOUNT_ACTION)(disconnect_account_callback)
