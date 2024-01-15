from slack_bolt import App
from .submit_pat import submit_pat_callback
from .clear_pat import clear_pat_callback


def register(app: App):
    app.action("submit_pat")(submit_pat_callback)
    app.action("clear_pat")(clear_pat_callback)
