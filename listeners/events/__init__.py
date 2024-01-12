from slack_bolt import App

from .app_home_open import app_home_open_callback


def register(app: App):
    app.event("app_home_opened")(app_home_open_callback)
