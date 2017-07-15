import json
from typing import List

from flask import current_app, request

from storage.getter import get_data
from datastore import devicedatatype

from twilio_util import notify_number
from datastore.device import maybe_update_is_connected


def data_event_handler():
    data = request.get_json()
    # This data is going to contain the json
    # representation of a DeviceData entry.
    device_id = data.get("device_id")
    maybe_update_is_connected(device_id)

    # Get data at location
    # Get previous data location
    # Get previous data at previous location
    # If previous data == closed and data == open, alarm
    # This data is an instance of DeviceData

    data_type_entity = devicedatatype.from_type_name(data['name'])
    if data_type_entity['type_name'] == "door":
        handle_door(data)
    return '', 204


def handle_door(data: dict):
    system_id = data['system_id']
    curr_location = data['location']
    phones = data['phones']

    prev_frames = data['previous']
    prev_locations = [f['location']
                      for f in prev_frames]

    if len(prev_locations) == 0:
        # Can't compare to anything so get out
        return

    curr_data = get_data(curr_location)
    curr_json = json.loads(curr_data)

    if curr_json.get('open'):
        raise_alarm(phones)


def raise_alarm(numbers: List[str]):
    for num in numbers:
        notify_number(num)

    # TODO: make use of grace period etc
