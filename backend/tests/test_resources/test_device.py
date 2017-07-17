import json
import uuid

import pytest


@pytest.fixture
def device_test_data(random_device, datatype_json):
    return dict(
        serial_number=random_device.serial_num,
        data={},
        type=datatype_json.type_name,
        ext="json"
    )


@pytest.fixture(autouse=True)
def mock_pubsub_request(monkeypatch):
    import mock
    monkeypatch.setattr('requests.post', mock.MagicMock())


def test_device_post(app, random_device, device_test_data):
    with app:
        resp = app.post('/api/device/data', data=json.dumps(device_test_data),
                        headers={'content-type': 'application/json'})

    assert resp.status_code == 200

    # Check that a new device data entry is in the database
    from models.device import DeviceData
    assert len(DeviceData.from_device(random_device)) != 0


def test_device_post_callspubsub(app, device_test_data):
    import requests
    with app.application.app_context():
        resp = app.post('/api/device/data', data=json.dumps(device_test_data),
                        headers={'content-type': 'application/json'})

    # noinspection PyUnresolvedReferences
    assert requests.post.called


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


def test_device_updating(logged_in_app, random_device):
    data = {
        "name": "somethingnew",
        "enabled": not random_device.enabled
    }
    url = "/api/device/{}".format(random_device.serial_num)

    assert random_device.name != data["name"]

    with logged_in_app:
        resp = logged_in_app.put(url, data=json.dumps(data),
                                 headers={'content-type': 'application/json'})
    assert resp.status_code == 200

    assert random_device.name == "somethingnew"
    assert random_device.enabled == data["enabled"]


def test_device_updating_badkeys(logged_in_app, random_device):
    data = {
        "serial_num": "fakeserial",
        "system_key": "12345",
        "is_connected": True,
        "device_type_key": 100
    }
    url = "/api/device/{}".format(random_device.serial_num)
    for k, v in data.items():
        with logged_in_app:
            resp = logged_in_app.put(url, data=json.dumps({k: v}),
                                     headers={'content-type': 'application/json'})
        assert resp.status_code != 200
        assert getattr(random_device, k) != v


def test_system_association(logged_in_app, random_system, random_device_nosystem,
                            random_owner):
    data = {
        'system_id': random_system.key.integer_id()
    }
    url = "/api/device/{}".format(random_device_nosystem.serial_num)

    assert random_device_nosystem.system_key is None

    with logged_in_app:
        resp = logged_in_app.put(url, data=json.dumps(data),
                                 headers={"content-type": "application/json"})
    assert resp.status_code == 200

    assert random_device_nosystem.system_key == random_system.key


def test_system_disassociation(logged_in_app, random_system, random_device,
                               random_owner):
    data = {
        'system_id': None
    }
    url = "/api/device/{}".format(random_device.serial_num)

    assert random_device.system_key == random_system.key

    with logged_in_app:
        resp = logged_in_app.put(url, data=json.dumps(data),
                                 headers={'content-type': 'application/json'})
    assert resp.status_code == 200

    new_device = random_device.key.get()
    assert new_device.system_key is None

