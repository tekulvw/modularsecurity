import cloudstorage as gcs
from storage import BUCKET_PREFIX

from models.device import Device

READ_RETRY = gcs.RetryParams(backoff_factor=1.1)


def get_latest_data_location(device):
    """
    Gets the url path to the latest data entry from a given device
    :param device: device datastore object
    :return: string
    """
    serial = device.serial_num
    base_path = BUCKET_PREFIX.format(serial)

    last_info = None

    for statinfo in gcs.listbucket(base_path, retry_params=READ_RETRY):
        last_info = statinfo

    try:
        filename = last_info.filename
    except AttributeError:
        raise RuntimeError("There are no files in the storage.")

    return filename


def get_next_data_location(device, ext=None):
    # type: (Device, str) -> str
    """
    Gets an unused url for the next data entry from a given device.
    :param device: Device datastore object
    :param ext:
    :return: string
    """
    raise NotImplementedError("Need to use os.path manipulations here.")

    try:
        last = get_latest_data_location(device)
    except RuntimeError:
        last = BUCKET_PREFIX.format(device.serial_num) + "/0"
        num = -1
    else:
        num = int(last[-1])

    num += 1

    return last[:-1] + str(num) + ".{}".format(ext) if ext else ""
