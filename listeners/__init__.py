from listeners import events, functions, actions


def register_listeners(app):
    functions.register(app)
    events.register(app)
    actions.register(app)
