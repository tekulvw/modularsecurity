from google.appengine.ext import ndb

from flask import jsonify, abort, request
from flask.views import MethodView
from flask_login import login_required, current_user

from models.owner import Owner as OwnerModel
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
    def update(self, system_id):
        data = request.get_json()
        if data is None:
            abort(401)

        raise NotImplementedError()

        current_user.update_from(data)
        return jsonify(current_user.to_json())
