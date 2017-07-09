import pytest
import sys
from models.user import User


def test_user_attrs():
    attrs = ("fname", "lname", "oauth_id", "phone_num", "create_date")
    assert all(hasattr(User, attr) for attr in attrs) is True


def test_real_json(random_user):
    import json
    assert random_user.to_json() == json.loads(json.dumps(random_user.to_json()))
