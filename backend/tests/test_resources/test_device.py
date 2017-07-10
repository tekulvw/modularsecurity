import json


def test_device_post(app, random_device):
    data = dict(
        serial_number=random_device.serial_num
    )

    with app:
        resp = app.post('/api/device', data=json.dumps(data), headers={'content-type': 'application/json'})

    assert resp.status_code == 200

    # Check that a new device data entry is in the database
    from models.device import Device
    assert Device.from_serial_number(random_device.serial_num) is not None
