import json
import os

from flask import session, current_app


def initialize_tokengetter(auth_obj):
    @auth_obj.tokengetter
    def tokengetter():
        auth_resp = session.get("authorization")
        if auth_resp:
            return auth_resp["access_token"], ''
        return None


def read_client_keys(path="client_secret.json"):
    """
    Reads client keys from client_keys.json
    :param path: path relative to CWD to find the keys file
    :return: tuple of (client_id, client_secret)
    """

    if not os.path.exists(path):
        raise RuntimeError("No oauth keys were found.")

    with open(path, 'r') as f:
        try:
            key_data = json.load(f)
        except ValueError:
            # Invalid JSON doc
            raise

    web_data = key_data.get("web")
    if web_data is None:
        raise RuntimeError("No valid web secret keys found.")

    client_id = web_data.get("client_id")
    client_secret = web_data.get("client_secret")

    return client_id, client_secret

