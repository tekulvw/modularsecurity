import json
import os
from twilio.rest import Client
from twilio.base.exceptions import TwilioRestException
from flask import current_app

import functools

CLIENT = None


def get_client():
    global CLIENT
    if CLIENT is None:
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
    my_num = current_app.config.get('TWILIO_NUMBER')
    client = get_client()
    sentry_client = current_app.config.get('SENTRY')
    try:
        client.messages.create(
            to=phone_number,
            from_=my_num,
            body="ALARM ALARM ALARM"
        )
    except TwilioRestException:
        sentry_client.captureException()
