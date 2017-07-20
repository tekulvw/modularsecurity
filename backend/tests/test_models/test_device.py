import pytest
from models.device import Device, DeviceData, DeviceDataType


def test_device_attrs():
    attrs = ("serial_num","system_key","name","is_connected","device_type_key")
    assert all(hasattr(Device, attr) for attr in attrs) is True


def test_device_real_json(random_device):
    import json
    assert random_device.to_json() == json.loads(json.dumps(random_device.to_json()))


def test_device_type_serialization(random_device):
    type_ = random_device.device_type_key.get()

    assert random_device.to_json()['type'] == type_.to_json()


def test_devicedata_attrs():
    attrs = ("location", "data_received", "device_key")
    assert all(hasattr(DeviceData, attr) for attr in attrs) is True


def test_devicedata_real_json(random_devicedata):
    import json
    assert random_devicedata.to_json() == json.loads(json.dumps(random_devicedata.to_json()))


def test_devicedata_get_last(random_device, random_devicedata):
    frames = DeviceData.get_last(random_device)
    assert random_devicedata in frames


def test_devicedata_get_last_counting(random_device):
    frames = DeviceData.get_last(random_device)
    assert len(frames) == 0

    frames = DeviceData.get_last(random_device, n=100)
    assert len(frames) == 0


def test_devicedatatype_attrs():
    attrs = ("type_name", )
    assert all(hasattr(DeviceDataType, attr) for attr in attrs) is True


