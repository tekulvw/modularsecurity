from models.user import User


def test_user_attrs():
    attrs = ("fname", "lname", "oauth_id", "phone_num", "create_date")
    assert all(hasattr(User, attr) for attr in attrs) is True
