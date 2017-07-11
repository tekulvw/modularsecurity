from flask import abort, request, jsonify
from flask.views import MethodView
from flask_login import login_required, current_user

from models.device import Device as DeviceModel
from models.device import DeviceData

from storage import store_data


class DeviceCollectionResource(MethodView):
    @login_required
    def post(self):
        if not current_user.is_admin:
            abort(401)

        data = request.get_json()
        serial_number = data.get("serial_number")
        if serial_number is None:
            abort(400)

        device = DeviceModel.create(serial_number)
        device.put()
        return jsonify(device.to_json())


class DeviceResource(MethodView):
    def post(self):
        # Request post json data
        data = request.get_json()

        # Abort if None
        if data is None:
            abort(400)

        # Gets serial number, then gets key from referencing serial number
        serial_number = data.get('serial_number')
        sensor_data = data.get('data')

        if serial_number is None or sensor_data is None:
            abort(400)
        device = DeviceModel.from_serial_number(serial_number)

        data_loc = store_data(device, sensor_data)

        # Creates a new entry for the data coming in then posts it
        entry = DeviceData.create(device.key)
        entry.location = data_loc
        entry.put()

        return jsonify({})
