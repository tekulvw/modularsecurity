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
