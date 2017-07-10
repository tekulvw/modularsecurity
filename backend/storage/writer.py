import json

import cloudstorage as gcs
import base64
from storage.getter import get_next_data_location

WRITE_RETRY = gcs.RetryParams(backoff_factor=1.1)


def store_data(device, data):
    """
    Stores data and returns the url to it.
    :param device: The device object from datastore
    :param data: raw data from device, will be stored B64 encoded
    :return: string
    """
    filename = get_next_data_location(device)
    dev_id = device.key.integer_id()
    gcs_file = gcs.open(filename=filename,
                        mode='w',
                        content_type='text/plain',  # This will need to be changed?
                        options={
                            'x-goog-meta-devid': str(dev_id)
                        },
                        retry_params=WRITE_RETRY)

    b64_data = base64.b64encode(json.dumps(data))

    gcs_file.write(b64_data)

    gcs_file.close()

    return filename
