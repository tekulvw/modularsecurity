import pytest
from models.owner import Owner


def test_attrs():
    attrs = ("user_key", "system_key")
    assert all(hasattr(Owner, attr) for attr in attrs) is True


def test_owner_create(random_user):
    owner = Owner.create(random_user.oauth_id, 60)
    owner.put()
