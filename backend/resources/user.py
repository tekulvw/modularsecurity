import calendar
import datetime
from flask import current_app as app
from flask import url_for, redirect, session, jsonify, flash, abort, request
from flask.views import MethodView
from flask_login import login_user, logout_user, login_required, current_user

from models.user import User as UserModel
from models.owner import Owner as OwnerModel
from models.secondary import Secondary


class AuthorizeUser(MethodView):
    def get(self):
        auth = app.config.get("AUTH")
        return auth.authorize(callback=url_for('authorized', _external=True))


class AuthorizedUser(MethodView):
    def get(self):
        auth = app.config.get("AUTH")
        resp = auth.authorized_response()

        if resp:
            now = datetime.datetime.utcnow()
            expires_in = int(resp.get("expires_in", 3600))
            expires_at = now + datetime.timedelta(seconds=expires_in)
            resp.update(expires_at=calendar.timegm(expires_at.timetuple()))
            session["authorization"] = resp
        return redirect(url_for('login'))


class UserInfo(MethodView):
    @login_required
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
        user = UserModel.from_oauth_id(userinfo.data['id'])
        if user is None:
            user = UserModel.create(userinfo)
            user.put()

            owner = OwnerModel.create(user, 60)
            owner.put()

        login_user(user)
        flash("Logged in!")
        return redirect('/loggedIn.html')


class Logout(MethodView):
    def get(self):
        logout_user()
        try:
            del session['authorization']
        except KeyError:
            pass
        return redirect(url_for('home'))


class User(MethodView):
    @login_required
    def get(self, oauth_id=None):
        """
        Gets current user information.
        :param oauth_id:
        :return: models/user/User plus owned_systems, secondary_systems
        """
        if oauth_id is None:
            oauth_id = current_user.oauth_id

        if current_user.oauth_id != oauth_id:
            # TODO: Check for admin status here.
            abort(403)

        data = current_user.to_json()
        owned = OwnerModel.from_user(current_user)
        try:
            owned_data = owned.system_key.get().to_json()
        except AttributeError:
            owned_data = {}
        data['owned_systems'] = [owned_data, ]

        secondary = Secondary.from_user(current_user)
        secondary_data = [s.system_key.get().to_json() for s in secondary]
        data['secondary_systems'] = secondary_data

        return jsonify(data)

    @login_required
    def put(self):
        """
        Keys sent must be a subset or equal to the keys in model/user/User
        :return: model/user/User
        """
        data = request.get_json()
        if data is None or not UserModel.valid_update_keys(data.keys()):
            abort(400)

        current_user.update_from(data)
        return jsonify(current_user.to_json())
