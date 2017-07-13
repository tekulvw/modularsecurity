from flask import request, abort, jsonify
from flask.views import MethodView

from flask_login import current_user, login_required

from models.user import User
from models.owner import Owner
from models.secondary import Secondary as SecondaryModel
from models.system import System


class Secondary(MethodView):
    @login_required
    def post(self):
        data = request.get_json()

        system_id = data.get('system_id')
        user_email = data.get('user_email')
        if None in (system_id, user_email):
            abort(400)

        system = System.from_system_id(system_id)
        user = User.from_email(user_email)

        if current_user == user:
            abort(400)

        if not Owner.is_owner_of(current_user, system):
            abort(401)

        sec_obj = SecondaryModel.create(user, system)
        sec_obj.put()
        return jsonify(current_user.to_json())

    @login_required
    def delete(self, system_id):
        data = request.get_json()
        user_email = data.get('user_email')

        system = System.from_system_id(system_id)
        user = User.from_email(user_email)

        if None in (system, user):
            abort(400)

        if not Owner.is_owner_of(current_user, system):
            abort(401)

        secondary = SecondaryModel.from_system_user(system, user)
        try:
            secondary.key.delete()
        except AttributeError:
            pass

        return jsonify({})
