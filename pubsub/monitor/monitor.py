from flask import current_app, request
import base64


def data_event_handler():
    data = request.get_json()
    print(request)
    return '', 204


def get_datastore_client():
    return current_app.config['DATASTORE_CLIENT']
