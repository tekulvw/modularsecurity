import pytest


def test_system_attrs():
    from models.system import System
    attrs = ("grace_period", "alarm_count", "ks_enabled", "create_date", "name")
    assert all(hasattr(System, attr) for attr in attrs) is True


def test_system_name(random_system):
    assert random_system.name is not None