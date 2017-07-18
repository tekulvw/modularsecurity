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

        if None in (system, user):
            abort(400)

        if current_user == user:
            abort(400)

        if not Owner.is_owner_of(current_user, system):
            abort(401)

        sec_obj = SecondaryModel.create(user, system)
        sec_obj.put()

        sec_users = SecondaryModel.get_all_secondary_users(system)
        return jsonify([u.to_json() for u in sec_users])

    @login_required
    def get(self, system_id):
        system = System.from_system_id(system_id)
        if system is None or not Owner.is_owner_of(current_user, system):
            abort(400)

        secondaries = SecondaryModel.from_system(system)

        ret = {}
        for s in secondaries:
            ret[s.key.integer_id()] = s.user_key.get().to_json()

        return jsonify(ret)

    @login_required
    def delete(self, secondary_id):
        secondary = SecondaryModel.from_id(secondary_id)
        if secondary is None:
            abort(400, "That secondary does not exist.")

        if not Owner.is_owner_of(current_user, secondary.system_key.get()):
            abort(401)

        try:
            secondary.key.delete()
        except AttributeError:
            pass

        return jsonify({})
