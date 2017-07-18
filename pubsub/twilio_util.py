import json
import os
from twilio.rest import Client

import functools

CLIENT = None


def get_client():
    if CLIENT is None:
        global CLIENT
        CLIENT = Client(*load_twilio_creds())
    return CLIENT


@functools.lru_cache()
def load_twilio_creds() -> (str, str):
    """
    Loads twilio creds from file.
    :return: AccountID, AuthToken
    """
    cred_path = os.environ.get("CONFIG_PATH") or "config.json"

    with open(cred_path) as f:
        data = json.load(f)

    twilio_data = data.get("TWILIO")
    acc_id = twilio_data.get("ACCOUNT_ID")
    api_key = twilio_data.get("AUTH_TOKEN")

    return acc_id, api_key


def notify_number(phone_number: str):
    client = get_client()
    client.messages.create(
        to=phone_number,
        from_=phone_number,
        body="ALARM ALARM ALARM"
    )
