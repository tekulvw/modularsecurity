from flask import current_app, request

from datastore import devicedatatype


def data_event_handler():
    data = request.get_json()
    data_type_entity = devicedatatype.from_type_name(data['name'])
    if data_type_entity['type_name'] == "door":
        handle_door(data)
    return '', 204


def handle_door(data: dict):
    curr_location = data['location']
    prev_location


def get_datastore_client():
    return current_app.config['DATASTORE_CLIENT']
