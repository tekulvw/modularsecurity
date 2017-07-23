import os

import cloudstorage as gcs
from storage import BUCKET_PREFIX

from models.device import Device

READ_RETRY = gcs.RetryParams(backoff_factor=1.1)

# Path is gonna look like:
# /devicedata/12345/0.json
# /devicedata/12345/1.png


def get_latest_data_location(device):
    # type: (Device) -> str
    """
    Gets the url path to the latest data entry from a given device
    :param device: device datastore object
    :return: string
    """
    serial = device.serial_num
    base_path = BUCKET_PREFIX.format(serial)

    filenames = []

    # This is probably wrong too. Damnit.
    for statinfo in gcs.listbucket(base_path, retry_params=READ_RETRY):
        filenames.append(statinfo.filename)

    split_filenames = [os.path.splitext(f) for f in filenames]

    with_index = [(int(os.path.split(f[0])[1]), f) for f in split_filenames]
    sorted_filenames = sorted(with_index, key=lambda e: e[0], reverse=True)

    try:
        index, split_filename = sorted_filenames[0]
    except IndexError:
        raise RuntimeError("There are no files in the storage.")

    filename = split_filename[0] + split_filename[1]

    return filename


def get_next_data_location(device):
    # type: (Device, str) -> str
    """
    Gets an unused url for the next data entry from a given device. WITHOUT EXTENSION.
    :param device: Device datastore object
    :return: string
    """

    try:
        last = get_latest_data_location(device)
    except RuntimeError:
        last = BUCKET_PREFIX.format(device.serial_num) + "/-1"

    filepath, ext = os.path.splitext(last)
    head, tail = os.path.split(filepath)
    num = int(tail)

    num += 1

    return os.path.join(head, str(num))


def get_download_url(location):
    download_url = "https://storage.googleapis.com{}".format(location)
    return download_url
