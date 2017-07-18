from raven.contrib.flask import Sentry


def load_sentry(app):
    return Sentry(app)
