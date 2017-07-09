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
    assert json.loads(resp.data) == random_user.to_json()


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
