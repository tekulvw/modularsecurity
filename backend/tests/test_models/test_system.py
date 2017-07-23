import pytest
from flask import url_for

from models.system import System
import json


def test_system_attrs():
    attrs = ("grace_period", "alarm_count", "ks_enabled","create_date")
    assert all(hasattr(System, attr) for attr in attrs) is True


def test_real_json(random_system):
    assert random_system.to_json() == json.loads(json.dumps(random_system.to_json()))


def test_system_from_id(random_system):
    assert random_system == System.from_system_id(random_system.key.integer_id())


def test_system_from_id_none():
    assert System.from_system_id(None) is None


def test_system_dataframes_empty(random_system):
    frames = random_system.get_latest_data_frames()
    assert len(frames) == 0


def test_system_dataframes_notempty(random_system, random_devicedata):
    frames = random_system.get_latest_data_frames()
    assert len(frames) > 0


def test_updatefrom_grace_baddata(random_system):
    # type: (System) -> None
    data = {
        "grace_period": "abcdef"
    }
    with pytest.raises(ValueError):
        random_system.update_from(data)


def test_updatefrom_str_grace(random_system):
    # type: (System) -> None
    data = dict(grace_period="20")
    random_system.update_from(data)

    assert random_system.grace_period == 20


def test_updatefrom_int_grace(random_system):
    # type: (System) -> None
    data = dict(grace_period=20)
    random_system.update_from(data)

    assert random_system.grace_period == 20


def test_download_urls(
        random_owner, random_system, random_device, random_devicedata,
        logged_in_app):
    user = random_owner.user_key.get()
    with logged_in_app.application.app_context():
        resp = logged_in_app.get(
            url_for('dataframe', system_id=random_system.key.integer_id())
        )

    assert resp.status_code == 200

    data = json.loads(resp.data)
    dev_serial = str(random_device.key.get().serial_num)
    assert dev_serial in data

    url = data.get(dev_serial)
    assert url.startswith('https://')

    assert 'appspot.com' in url
