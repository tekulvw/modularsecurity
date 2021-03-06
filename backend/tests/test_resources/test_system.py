import json

import pytest
from models.device import Device
from models.device import DeviceData
from flask import url_for


def test_key_not_none(random_system):
    from google.appengine.ext import ndb
    assert random_system.key is not None
    assert isinstance(random_system.key, ndb.Key)


def test_system_get(logged_in_app, random_system):
    args = dict(
        system_id=random_system.key.integer_id()
    )

    with logged_in_app.application.app_context():
        resp = logged_in_app.get(url_for('system', **args))
    assert json.loads(resp.data) == random_system.to_json()


def test_system_post(logged_in_app, random_system, random_user):
    data = dict(
        oauth_id=random_user.oauth_id,
        grace_period=random_system.grace_period
    )

    with logged_in_app:
        resp = logged_in_app.post('/api/system', data=json.dumps(data), headers={'content-type': 'application/json'})

    assert resp.status_code == 200


def system_put(app, system_id, data):
    with app.application.app_context():
        resp = app.put(url_for('system', system_id=system_id), data=json.dumps(data),
                       headers={'content-type': 'application/json'})
    return resp


def test_system_put_nologin(app, random_owner, random_system):
    data = dict(name="SOMEThING NEw")
    resp = system_put(app, random_system.key.integer_id(), data)

    assert resp.status_code == 401
    assert random_system.name != data.get('name')


def test_system_put(logged_in_app, random_owner, random_system):
    update_data = {
        "name": "ERIC"
    }

    resp = system_put(logged_in_app, random_system.key.integer_id(), update_data)

    assert resp.status_code == 200
    new_system = random_system.key.get()
    assert new_system.name == "ERIC"


def test_system_put_strgrace(logged_in_app, random_owner, random_system):
    data = dict(grace_period="20")

    resp = system_put(logged_in_app, random_system.key.integer_id(), data)

    assert resp.status_code == 200
    assert random_system.grace_period == 20


def test_system_put_nonowner(logged_in_app, random_system):
    update_data = {
        "name": "notdefault"
    }
    assert random_system.name != update_data['name']
    with logged_in_app.application.app_context():
        resp = logged_in_app.put(
            url_for('system', system_id=random_system.key.integer_id()),
            data=json.dumps(update_data),
            headers={'content-type': 'application/json'}
        )
    assert resp.status_code == 401
    assert random_system.name != update_data['name']


def test_dataframes_get(logged_in_app, random_owner, random_devicedata):
    system_key = random_owner.system_key
    with logged_in_app.application.app_context():
        resp = logged_in_app.get(
            url_for('dataframe', system_id=system_key.integer_id())
        )
    data = json.loads(resp.data)
    device = random_devicedata.device_key.get()
    assert resp.status_code == 200
    assert device.serial_num in data


def test_killswitch_put(logged_in_app, random_system, random_owner):
    update_data = {
        "ks_enabled": True
    }
    with logged_in_app:
        resp = logged_in_app.put('/api/system/%d/killswitch' % random_system.key.integer_id(),
                                 data=json.dumps(update_data),
                                 headers={'content-type': 'application/json'})
    assert resp.status_code == 200
    new_system = random_system.key.get()
    assert new_system.ks_enabled is True


def test_killswitch_put_nonowner(logged_in_app, random_system):
    update_data = {
        "ks_enabled": True
    }

    assert random_system.ks_enabled is False

    with logged_in_app.application.app_context():
        resp = logged_in_app.put(url_for('killswitch', system_id=random_system.key.integer_id(),
                                         data=json.dumps(update_data),
                                         headers={'content-type': 'application/json'}))
    assert resp.status_code == 401
    assert random_system.ks_enabled is False
