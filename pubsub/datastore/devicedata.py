from datastore import client
from google.cloud.datastore import Key


def get_last_dataframes(device_id: int, n: int=1):
    key = Key("Device", device_id)
    device = client.get(key)

    q = client.query(kind="DeviceData")
    q.add_filter("device_key", "=", device.key)
