import json


def test_device_post(app, random_device):
    data = dict(
        serial_number=random_device.serial_num
    )

    with app:
        resp = app.post('/api/device', data=json.dumps(data), headers={'content-type': 'application/json'})

    assert resp.status_code == 200

    # Check that a new device data entry is in the database

    #assert app.query(resp.serial_ == random_device.serial_num)
    #assert app.json == random_device.serial_num
    assert json.loads(resp.data).get('serial_num') == random_device.to_json().get('serial_num')