from storage import client

from pathlib import Path

from flask import current_app


def get_data(location: str) -> str:
    """
    Location needs to be in form /bucket_name/path/to/blob.txt
    :param location:
    :return: data
    """
    location = Path(location)
    bucket_name, blob_parts = location.parts[1], location.parts[2:]

    blob_path = '/'.join(blob_parts)

    bucket = client.bucket(bucket_name=bucket_name)
    data = None
    if not current_app.config.get('TESTING'):
        blob = bucket.get_blob(blob_path)
        if blob is not None:
            data = blob.download_as_string()

    if data is None:
        data = '{"open": "1"}'
    return data
