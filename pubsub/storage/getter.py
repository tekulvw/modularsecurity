from google.cloud import storage
from storage import client

from pathlib import Path
import json


def get_previous_location(current_location: str) -> str:
    pass


def get_data(location: str) -> object:
    """
    Location needs to be in form /bucket_name/path/to/blob.txt
    :param location:
    :return: data
    """
    location = Path(location)
    bucket_name, blob_parts = location.parts[0], location.parts[1:]

    blob_path = '/' + '/'.join(blob_parts)

    bucket = client.bucket(bucket_name=bucket_name)
    blob = bucket.get_blob(blob_path)

    data = blob.download_as_string()
    return json.loads(data)
