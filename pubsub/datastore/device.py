from datastore import client
from google.cloud.datastore import Key, Entity


def from_device_id(device_id: int) -> Entity:
    key = Key("Device", device_id)
    entity = client.get(key)
    if entity is None:
        raise RuntimeError("No such device with id {}".format(device_id))
    return entity


def maybe_update_is_connected(device_id: int):
    try:
        device = from_device_id(device_id)
    except RuntimeError:
        return

    is_connected = device['is_connected']
    if not is_connected:
        device['is_connected'] = True
        client.put(device)
