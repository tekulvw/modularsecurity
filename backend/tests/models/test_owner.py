import pytest


@pytest.fixture
def owner_cls():
    from models.owner import Owner
    return Owner


def test_attrs(owner_cls):
    attrs = ("user_key", "system_key")
    assert all(hasattr(owner_cls, attr) for attr in attrs) is True
