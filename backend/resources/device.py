from flask import abort, request, jsonify
from flask.views import MethodView
from flask_login import login_required, current_user

from models.device import Device as DeviceModel
from models.device import DeviceData, DeviceDataType
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
    def get_system_info(self, system, modified=None):
        data = system.to_json()
        devices = DeviceModel.from_system_key(system.key)
        return data, devices

    def post(self):
        # Request post json data
        data = request.get_json()

        # Abort if None
        if data is None:
            abort(400, "Missing required data.")

        # Gets serial number, then gets key from referencing serial number
        serial_number = data.get('serial_number')
        sensor_data = data.get('data')
        ext = data.get('ext')
        type_ = data.get('type')

        if None in (serial_number, sensor_data, ext, type_):
            abort(400, "Missing required data field.")

        device = DeviceModel.from_serial_number(serial_number)
        data_type = DeviceDataType.from_name(type_)

        if None in (device, data_type):
            abort(400, "No matching device or type in datastore.")

        data_loc = store_data(device, sensor_data, data_type, ext)

        # Creates a new entry for the data coming in then posts it
        entry = DeviceData.create(device.key)
        entry.location = data_loc
        entry.put()

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

        if system is None and curr_system is None:
            abort(400, 'No valid systems.')

        if not all(Owner.is_owner_of(current_user, s)
                   for s in (system, curr_system)
                   if s is not None):
            abort(401)

        try:
            device.system_key = system.key
        except AttributeError:
            device.system_key = None

        device.put()
        return (curr_system or system), device

    @login_required
    def put(self, serial_number):
        data = request.get_json()
        if "system_id" in data:
            system, device = self.update_device_association(serial_number, data)
        else:
            device = DeviceModel.from_serial_number(serial_number)
            if device is None:
                abort(400)

            try:
                device.update_from(data)
            except RuntimeError:
                abort(400)

            system = device.system_key.get()
        data, devices = self.get_system_info(system)
        if device in devices:
            devices.remove(device)
        devices.append(device)
        data['devices'] = [d.to_json()
                           for d in devices]
        return jsonify(data)
