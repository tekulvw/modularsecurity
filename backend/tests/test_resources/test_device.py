import json
import uuid

import pytest


@pytest.fixture
def device_test_data(random_device):
    return dict(
        serial_number=random_device.serial_num,
        data={}
    )


def test_device_post(app, random_device, device_test_data):
    with app:
        resp = app.post('/api/device/data', data=json.dumps(device_test_data),
                        headers={'content-type': 'application/json'})

    assert resp.status_code == 200

    # Check that a new device data entry is in the database
    from models.device import DeviceData
    assert len(DeviceData.from_device(random_device)) != 0


def test_device_post_nocontenttype(app, random_device, device_test_data):
    with app:
        resp = app.post('/api/device/data', data=json.dumps(device_test_data))

    assert resp.status_code == 400

    from models.device import DeviceData
    assert len(DeviceData.from_device(random_device)) == 0


def test_malformed_data(app):
    with app:
        resp = app.post('/api/device/data', data="{}",
                        headers={"content-type": "application/json"})

    assert resp.status_code == 400


def test_device_creation(admin_app):
    serial_number = str(uuid.uuid4())
    post_data = {
        "serial_number": serial_number
    }

    with admin_app:
        resp = admin_app.post('/api/device', data=json.dumps(post_data),
                              headers={"content-type": "application/json"})

    assert resp.status_code == 200

    from models.device import Device
    assert Device.from_serial_number(serial_number) is not None