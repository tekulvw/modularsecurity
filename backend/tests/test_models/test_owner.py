import pytest
from models.owner import Owner


def test_attrs():
    attrs = ("user_key", "system_key")
    assert all(hasattr(Owner, attr) for attr in attrs) is True


def test_owner_create(random_user):
    owner = Owner.create(random_user, 60)
    owner.put()

    assert owner.user_key == random_user.key
    assert owner.system_key is not None

    system = owner.system_key.get()
    assert system.grace_period == 60


def test_owner_from_system(random_owner, random_system):
    assert Owner.from_system(random_system) == random_owner


def test_owner_contact_number(random_owner):
    user = random_owner.user_key.get()

    assert random_owner.get_contact_number() == user.phone_num
