from models.owner import Owner


def test_attrs():
    attrs = ("user_key", "system_key")
    assert all(hasattr(Owner, attr) for attr in attrs) is True
