import os

import pytest


@pytest.fixture
def device_data_location(random_device, datatype_json):
    from storage.writer import store_data
    return store_data(random_device, {}, datatype_json, "json")


def test_starting_location_no_files(random_device):
    from storage.getter import get_next_data_location

    next_loc = get_next_data_location(random_device)
    assert next_loc.endswith("0")


def test_last_location_no_files(random_device):
    from storage.getter import get_latest_data_location

    with pytest.raises(RuntimeError):
        get_latest_data_location(device=random_device)


def test_with_files(random_device, device_data_location,
                    datatype_json):
    filepath, ext = os.path.splitext(device_data_location)
    assert filepath.endswith("0")

    from storage.writer import store_data
    for i in range(1, 5):
        next_location = store_data(random_device, {"hi": "world"},
                                   type=datatype_json,
                                   extension="json")

        filepath, ext = os.path.splitext(next_location)

        assert filepath.endswith(str(i))

