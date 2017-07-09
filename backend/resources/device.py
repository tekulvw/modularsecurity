from flask import abort, request
from flask.views import MethodView

from models.device import Device as DeviceModel
from models.device import DeviceData


class Device(MethodView):
    def post(self):
        # Request post json data
        data = request.get_json()

        # Abort if None
        if data is None:
            abort(401)

        # Gets serial number, then gets key from referencing serial number
        serial_number = data.get('serial_number')
        key = DeviceModel.from_serial_number(serial_number)

        # Creates a new entry for the data coming in then posts it
        entry = DeviceData.create(key)
        entry.put()
