from flask import url_for
import json

from models.secondary import Secondary


def test_secondary_post(random_owner, logged_in_app,
                        user_factory):
    other_user = user_factory.get()
    data = {
        "user_email": other_user.email,
        "system_id": random_owner.system_key.integer_id()
    }
    with logged_in_app.application.app_context():
        resp = logged_in_app.post(url_for('secondary'), data=json.dumps(data),
                                  headers={'content-type': 'application/json'})

    assert resp.status_code == 200

    is_secondary, model = Secondary.is_secondary_of(
        other_user, random_owner.system_key.get()
    )

    assert is_secondary is True


def test_secondary_get(random_owner, random_system, logged_in_app, user_factory):
    other_user = user_factory.get()
    sec = Secondary.create(other_user, random_system)
    sec.put()

    with logged_in_app.application.app_context():
        resp = logged_in_app.get(
            url_for('secondary', system_id=random_system.key.integer_id())
        )

    assert resp.status_code == 200

    data = json.loads(resp.data)

    for k, v in data.items():
        assert k == str(sec.key.integer_id())
        assert v == other_user.to_json()


def test_secondary_delete(random_owner, user_factory, logged_in_app):
    other_user = user_factory.get()
    sec = Secondary.create(other_user, random_owner.system_key.get())
    sec.put()

    is_sec, sec_obj = Secondary.is_secondary_of(other_user, random_owner.system_key.get())
    assert is_sec is True

    with logged_in_app.application.app_context():
        resp = logged_in_app.delete(
            url_for('secondary', secondary_id=sec_obj.key.integer_id())
        )

    assert resp.status_code == 200

    is_sec, _ = Secondary.is_secondary_of(other_user, random_owner.system_key.get())
    assert is_sec is False
