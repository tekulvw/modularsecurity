from typing import Union

from datastore import client
from google.cloud import datastore


def from_type_name(name: str) -> Union[datastore.Entity, None]:
    """
    Gets a DeviceDataType entity from the datastore using
        the type name.
    :param name:
    :return:
    """
    q = client.query(kind='DeviceDataType')
    q.add_filter('type_name', '=', name)
    return q.fetch(1)


def from_device_id(device_id: int) -> Union[datastore.Entity, None]:
    """
    Gets a DeviceDataType entity from the datastore using the device
        integer ID.
    :param device_id:
    :return:
    """
    key = datastore.Key('Device', device_id)
    device = client.get(key)

    try:
        type_key = device.device_type_key
    except AttributeError:
        return None

    data_type = client.get(type_key)
    return data_type
