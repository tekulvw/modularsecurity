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
