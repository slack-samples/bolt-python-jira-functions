from listeners import actions, events, functions


def register_listeners(app):
    functions.register(app)
    events.register(app)
    actions.register(app)
