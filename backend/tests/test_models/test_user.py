import pytest
import sys
from models.user import User


def test_user_attrs():
    attrs = ("fname", "lname", "oauth_id", "phone_num", "create_date")
    assert all(hasattr(User, attr) for attr in attrs) is True


def test_real_json(random_user):
    import json
    assert random_user.to_json() == json.loads(json.dumps(random_user.to_json()))


def test_from_oauth_id(random_user):
    user = User.from_oauth_id(random_user.oauth_id)
    assert user is not None
    assert user.oauth_id == random_user.oauth_id


def test_ensure_phone_string(random_user):
    assert isinstance(random_user.phone_num, basestring)
