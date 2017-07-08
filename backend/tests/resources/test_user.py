import pytest


@pytest.fixture
def random_user():
    from models import User
    import uuid
    user = User(
        fname="FirstName",
        lname="LastName",
        phone_num=0000000000,
        oauth_id=str(uuid.uuid4())
    )
    user.put()
    yield user
    user.key.delete()


def test_key_not_none(random_user):
    from google.appengine.ext import ndb
    assert random_user.key is not None
    assert isinstance(random_user.key, ndb.Key)


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
