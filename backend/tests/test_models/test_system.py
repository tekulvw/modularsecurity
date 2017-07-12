import pytest


def test_system_attrs():
    from models.system import System
    attrs = ("grace_period", "alarm_count", "ks_enabled","create_date")
    assert all(hasattr(System, attr) for attr in attrs) is True


def test_real_json(random_system):
    import json
    assert random_system.to_json() == json.loads(json.dumps(random_system.to_json()))


def test_system_from_id(random_system):
    from models.system import System
    assert random_system == System.from_system_id(random_system.key.integer_id())
