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


def test_secondary_delete(random_owner, user_factory, logged_in_app):
    other_user = user_factory.get()
    data = {
        "user_email": other_user.email
    }
    sec = Secondary.create(other_user, random_owner.system_key.get())
    sec.put()

    is_sec, _ = Secondary.is_secondary_of(other_user, random_owner.system_key.get())
    assert is_sec is True

    with logged_in_app.application.app_context():
        resp = logged_in_app.delete(
            url_for('secondary', system_id=random_owner.system_key.integer_id()),
            data=json.dumps(data), headers={'content-type': 'application/json'}
        )

    assert resp.status_code == 200

    is_sec, _ = Secondary.is_secondary_of(other_user, random_owner.system_key.get())
    assert is_sec is False
