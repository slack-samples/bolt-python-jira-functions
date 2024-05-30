from listeners import actions, events, functions


def register_listeners(app):
    actions.register(app)
    events.register(app)
    functions.register(app)
