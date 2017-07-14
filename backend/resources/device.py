from flask import abort, request, jsonify, current_app
from flask.views import MethodView
from flask_login import login_required, current_user

import requests

from models.device import Device as DeviceModel
from models.device import DeviceData
from models.system import System

from models.owner import Owner

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

        # PubSub stuff
        data = entry.to_json()
        pubsub_url = current_app.config['PUBSUB_URL']
        requests.post(pubsub_url, json=data,
                      headers={'content-type': 'application/json'})

        return jsonify({})

    def update_device_association(self, serial_number, req_data):
        system_id = req_data.get("system_id")
        system = System.from_system_id(system_id)
        device = DeviceModel.from_serial_number(serial_number)

        if device is None:
            abort(400)

        try:
            curr_system = device.system_key.get()
        except AttributeError:
            curr_system = None

        if not any(Owner.is_owner_of(current_user, s)
                   for s in (system, curr_system)):
            abort(403)

        try:
            device.system_key = system.key
        except AttributeError:
            device.system_key = None

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
