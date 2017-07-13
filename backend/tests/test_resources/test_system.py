import json

import pytest
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


def test_system_put(logged_in_app, random_owner, random_system):
    update_data = {
        "name": "ERIC"
    }
    with logged_in_app:
        resp = logged_in_app.put('/api/system/%d' %random_system.key.integer_id(), data=json.dumps(update_data),
                                 headers={'content-type': 'application/json'})

    assert resp.status_code == 200
    new_system = random_system.key.get()
    assert new_system.name == "ERIC"


@pytest.mark.skip(reason="Requires PR#101 in order to test.")
def test_system_put_nonowner():
    pass


def test_killswitch_put(logged_in_app, random_system):
    update_data = {
        "ks_enabled": True
    }
    with logged_in_app:
        resp = logged_in_app.put('/api/system/%d/killswitch' %random_system.key.integer_id(), data=json.dumps(update_data),
                                 headers={'content-type':'application/json'})
        assert resp.status_code == 200
        new_system = random_system.key.get()
        assert new_system.ks_enabled is True