from flask import current_app as app
from flask import url_for
from flask.views import MethodView


class AuthorizeUser(MethodView):
    def get(self):
        auth = app.config.get("AUTH")
        return auth.authorize(callback=url_for('home', _external=True))
