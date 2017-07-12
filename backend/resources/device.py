from flask import abort, request, jsonify
from flask.views import MethodView
from flask_login import login_required, current_user

from models.device import Device as DeviceModel
from models.device import DeviceData
from models.system import System

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

    def update_device_association(self, serial_number, req_data):
        system_id = req_data.get("system_id")
        system = System.from_system_id(system_id)
        device = DeviceModel.from_serial_number(serial_number)

        if system is None or device is None:
            abort(400)

        if device.system_key is not None:
            abort(403)

        device.system_key = system.key
        device.put()
        return jsonify(device.to_json())

    @login_required
    def put(self, serial_number):
        data = request.get_json()
        if "system_id" in data:
            return self.update_device_association(serial_number, data)
        else:
            device = DeviceModel.from_serial_number(serial_number)
            if device is None:
                abort(400)

            try:
                device.update_from(data)
            except RuntimeError:
                abort(400)

            return jsonify(device.to_json())
