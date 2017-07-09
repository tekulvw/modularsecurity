import pytest



@pytest.fixture
def system_cls():
    from models.system import System
    return System


def test_system_attrs(system_cls):
    attrs = ("grace_period", "alarm_count", "ks_enabled","create_date")
    assert all(hasattr(system_cls, attr) for attr in attrs) is True