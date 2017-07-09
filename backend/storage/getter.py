import cloudstorage as gcs
from storage import BUCKET_PREFIX

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
        filename = base_path + "/0"

    return filename


def get_next_data_location(device):
    """
    Gets an unused url for the next data entry from a given device.
    :param device: Device datastore object
    :return: string
    """
    last = get_latest_data_location(device)
    num = int(last[-1])

    num += 1

    return last[:-1] + str(num)