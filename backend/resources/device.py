from flask import current_app as app
from flask import url_for, redirect, session, jsonify, flash, abort, request
from flask.views import MethodView

from models import device

class Device(MethodView):
    def post(self):
        #serial_number = Device.serial_num()
        data = request.get_json()
        if data is None:
            abort(401)
        serial_number = data.get('serial_number')
        key = from_device_serial_number(serial_number)
        entry=device.create(key,data)
        entry.put()
