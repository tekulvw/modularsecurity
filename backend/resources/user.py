from flask import current_app as app
from flask import url_for, redirect
from flask.views import MethodView


class AuthorizeUser(MethodView):
    def get(self):
        auth = app.config.get("AUTH")
        return auth.authorize(callback=url_for('authorized', _external=True)), 302


class AuthorizedUser(MethodView):
    def get(self):
        auth = app.config.get("AUTH")
        resp = auth.authorized_response()

        if resp:
            # Authentication didn't fail
            pass
        return redirect(url_for('home'))
