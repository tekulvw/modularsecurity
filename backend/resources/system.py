from flask import jsonify, abort, request
from flask.views import MethodView
from flask_login import login_required, current_user

from models.owner import Owner as OwnerModel
from models.secondary import Secondary as SecondaryModel
from models.user import User as UserModel
from models.system import System as SystemModel


class System(MethodView):
    # @login_required
    def get(self, system_id):
        """
        :param system_id:
        :return: is_connected, type_id, latest_data
        """
        data = SystemModel.get_by_id(system_id)
        return jsonify(data.to_json())

    @login_required
    def post(self):
        data = request.get_json()
        if data is None:
            abort(401)
        grace = data.get('grace_period')
        oauth = data.get('oauth_id')
        user = UserModel.from_oauth_id(oauth_id=oauth)
        entry = OwnerModel.create(user, grace)
        entry.put()
        return jsonify({})

    @login_required
    def put(self, system_id):
        data = request.get_json()
        if data is None or not SystemModel.valid_update_keys(data.keys()):
            abort(401)

        current_system = SystemModel.get_by_id(system_id)
        if not OwnerModel.is_owner_of(current_user, current_system):
            abort(401)

        current_system.update_from(data)
        return jsonify(current_system.to_json())


class KillSwitch(MethodView):
    @login_required
    def put(self, system_id):
        data = request.get_json()
        if data is None or not SystemModel.valid_update_keys(data.keys()):
            abort(401)

        ks_status = data.get("ks_enabled")
        if ks_status is None:
            abort(400)

        current_system = SystemModel.get_by_id(system_id)

        owner = OwnerModel.is_owner_of(current_user, current_system)
        is_sec, _ = SecondaryModel.is_secondary_of(current_user, current_system)

        if not (owner or is_sec):
            abort(401)

        current_system.ks_enabled = ks_status
        current_system.put()

        return jsonify(current_system.to_json())
