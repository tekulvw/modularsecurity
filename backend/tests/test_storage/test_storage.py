import pytest


@pytest.fixture
def device_data_location(random_device):
    from storage.writer import store_data
    return store_data(random_device, {})


def test_starting_location_no_files(random_device):
    from storage.getter import get_next_data_location

    next_loc = get_next_data_location(random_device)
    assert next_loc.endswith("0")


def test_last_location_no_files(random_device):
    from storage.getter import get_latest_data_location

    with pytest.raises(RuntimeError):
        get_latest_data_location(device=random_device)


def test_with_files(random_device, device_data_location):
    assert device_data_location.endswith("0")

    from storage.writer import store_data
    next_location = store_data(random_device, {"hi": "world"})

    assert next_location.endswith("1")

