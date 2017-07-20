import json


def test_key_not_none(random_user):
    from google.appengine.ext import ndb
    assert random_user.key is not None
    assert isinstance(random_user.key, ndb.Key)


def test_random_user_in_db(random_user):
    from models.user import User
    assert random_user == User.from_oauth_id(random_user.oauth_id)


def test_user_get(logged_in_app, random_user):
    with logged_in_app:
        resp = logged_in_app.get('/api/user', follow_redirects=True)
    data = json.loads(resp.data)
    assert data['owned_systems'] == []
    assert data['secondary_systems'] == []

    del data['owned_systems']
    del data['secondary_systems']

    assert data == random_user.to_json()


def test_user_update(logged_in_app, random_user):
    update_data = {
        "fname": "UPDATED",
        "phone_num":"5135044350"
    }
    with logged_in_app:
        resp = logged_in_app.put('/api/user/', data=json.dumps(update_data),
                                 headers={'content-type': 'application/json'})

    assert resp.status_code == 200

    from models.user import User
    assert User.from_oauth_id(random_user.oauth_id).fname == "UPDATED"

def test_user_phone_update(logged_in_app, random_user):
    update_data = {
        "phone_num": "51350443501"
    }
    with logged_in_app:
        resp = logged_in_app.put('/api/user/', data=json.dumps(update_data),
                                 headers={'content-type': 'application/json'})

    assert resp.status_code == 400


"""
@pytest.fixture
def logged_in_user(random_user):
    from flask_login import login_user, logout_user
    login_user(random_user)
    yield random_user
    logout_user()


def test_login(logged_in_user):
    from flask_login import current_user
    assert current_user.oauth_id == logged_in_user.oauth_id
"""
