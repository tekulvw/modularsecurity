import json
import pytest


@pytest.fixture
def device_test_data(random_device):
    return dict(
        serial_number=random_device.serial_num,
        data={}
    )


def test_device_post(app, random_device, device_test_data):
    with app:
        resp = app.post('/api/device', data=json.dumps(device_test_data),
                        headers={'content-type': 'application/json'})

    assert resp.status_code == 200

    # Check that a new device data entry is in the database
    from models.device import DeviceData
    assert len(DeviceData.from_device(random_device)) != 0


def test_device_post_nocontenttype(app, random_device, device_test_data):
    with app:
        resp = app.post('/api/device', data=json.dumps(device_test_data))

    assert resp.status_code == 400

    from models.device import DeviceData
    assert len(DeviceData.from_device(random_device)) == 0


def test_malformed_data(app):
    with app:
        resp = app.post('/api/device', data="{}",
                        headers={"content-type": "application/json"})

    assert resp.status_code == 400
