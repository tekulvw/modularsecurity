def test_starting_location(random_device):
    from storage.getter import get_next_data_location

    next_loc = get_next_data_location(random_device)
    assert next_loc.endswith("1")


def test_last_location(random_device):
    from storage.getter import get_latest_data_location
    loc = get_latest_data_location(device=random_device)

    assert loc.endswith("0")
