from flask import current_app as app
from flask import url_for, redirect, session
from flask.views import MethodView


class AuthorizeUser(MethodView):
    def get(self):
        auth = app.config.get("AUTH")
        return auth.authorize(callback=url_for('authorized', _external=True))


class AuthorizedUser(MethodView):
    def get(self):
        auth = app.config.get("AUTH")
        resp = auth.authorized_response()

        if resp:
            session["authorization"] = (resp, '')
        return redirect(url_for('home'))
