from slack_bolt import App

from .clear_pat import clear_pat_callback
from .oauth_url import oauth_url_callback
from .submit_pat import submit_pat_callback


def register(app: App):
    app.action("submit_pat")(submit_pat_callback)
    app.action("clear_pat")(clear_pat_callback)
    app.action("oauth_url")(oauth_url_callback)
