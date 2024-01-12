from listeners import events, functions


def register_listeners(app):
    functions.register(app)
    events.register(app)
