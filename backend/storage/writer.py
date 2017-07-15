import binascii
import json

import cloudstorage as gcs
from storage.getter import get_next_data_location

from models.device import Device, DeviceDataType

WRITE_RETRY = gcs.RetryParams(backoff_factor=1.1)


def store_data(device, data, type, extension):
    # type: (Device, object, DeviceDataType, str) -> str
    """
    Stores data and returns the url to it.
    :param device: The device object from datastore
    :param data: raw data from device, should be json or binary data
    :param type: DeviceDataType object from datastore
    :param extension: file extension for data WITHOUT PERIOD - string
    :return: string of location
    """
    filename = get_next_data_location(device) + "." + extension
    dev_id = device.key.integer_id()

    if type.is_binary:
        mode = 'wb'
        data = binascii.a2b_base64(data)
    else:
        mode = 'w'
        data = json.dumps(data)

    gcs_file = gcs.open(filename=filename,
                        mode=mode,
                        content_type=type.mime_type,
                        options={
                            'x-goog-meta-devid': str(dev_id)
                        },
                        retry_params=WRITE_RETRY)

    gcs_file.write(data)

    gcs_file.close()

    return filename
