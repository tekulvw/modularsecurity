import os
from google.appengine.api import app_identity

__all__ = ["store_data", ]

BUCKET_NAME = os.environ.get("BUCKET_NAME", app_identity.get_default_gcs_bucket_name())

BUCKET_PREFIX = "/" + BUCKET_NAME + ".appspot.com/devicedata/{}"

from .writer import store_data
