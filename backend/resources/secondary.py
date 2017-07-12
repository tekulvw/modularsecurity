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
        user_id = data.get('user_id')
        if None in (system_id, user_id):
            abort(400)

        system = System.from_system_id(system_id)
        user = User.from_oauth_id(user_id)

        if not Owner.is_owner_of(current_user, system):
            abort(401)

        sec_obj = SecondaryModel.create(user, system)
        sec_obj.put()
        return jsonify(sec_obj.to_json())


