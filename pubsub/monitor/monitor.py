import json

from flask import current_app, request

from storage.getter import get_data
from datastore import devicedatatype


def data_event_handler():
    data = request.get_json()
    # This data is an instance of DeviceData
    data_type_entity = devicedatatype.from_type_name(data['name'])
    if data_type_entity['type_name'] == "door":
        handle_door(data)
    return '', 204


def handle_door(data: dict):
    system_id = data['system_id']
    curr_location = data['location']

    prev_frames = data['previous']
    prev_locations = [f['location']
                      for f in prev_frames]

    if len(prev_locations) == 0:
        # Can't compare to anything so get out
        return

    curr_data = get_data(curr_location)
    curr_json = json.loads(curr_data)

    if curr_json.get('open'):
        raise_alarm()


def raise_alarm(system_id: int):
    pass
