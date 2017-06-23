import pytest
import sys


@pytest.fixture
def user_cls():
    from models.user import User
    return User


def test_user_attrs(user_cls):
    attrs = ("fname", "lname", "oauth_id", "phone_num", "create_date")
    assert all(hasattr(user_cls, attr) for attr in attrs) is True
