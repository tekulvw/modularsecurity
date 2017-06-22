from flask import current_app as app
from flask import url_for, redirect, session, jsonify, flash
from flask.views import MethodView
from flask_login import login_user, logout_user

from models import User


class AuthorizeUser(MethodView):
    def get(self):
        auth = app.config.get("AUTH")
        return auth.authorize(callback=url_for('authorized', _external=True))


class AuthorizedUser(MethodView):
    def get(self):
        auth = app.config.get("AUTH")
        resp = auth.authorized_response()

        if resp:
            session["authorization"] = resp
        return redirect(url_for('login'))


class UserInfo(MethodView):
    def get(self):
        auth = app.config.get("AUTH")
        data = auth.get('userinfo')
        return jsonify({'data': data.data})


class Login(MethodView):
    def get(self):
        auth = app.config.get("AUTH")

        if "authorization" not in session:
            return redirect(url_for('authorize'))

        userinfo = auth.get('userinfo')
        user = User.from_oauth_id(userinfo.data['id'])
        if user is None:
            user = User.create(userinfo)
            user.put()

        login_user(user)
        flash("Logged in!")
        return redirect(url_for('home'))


class Logout(MethodView):
    def get(self):
        logout_user()
        try:
            del session['authorization']
        except KeyError:
            pass
        return redirect(url_for('home'))
