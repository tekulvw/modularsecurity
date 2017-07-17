import os
from raven.contrib.flask import Sentry


def is_testing():
    # type: () -> bool
    return bool(os.environ.get("TESTING"))


def load_sentry(app):
    # type: (object) -> Sentry
    if is_testing():
        return

    return Sentry(app)
