import calendar
import datetime
from flask_oauthlib.client import OAuth
from flask import session, current_app


def initialize(app):
    oauth = OAuth(app)

    google = oauth.remote_app(
        'google',
        consumer_key=app.config.get('GOOGLE_ID'),
        consumer_secret=app.config.get('GOOGLE_SECRET'),
        request_token_params={
            'scope': 'email'
        },
        base_url='https://www.googleapis.com/oauth2/v1/',
        request_token_url=None,
        access_token_method='POST',
        access_token_url='https://accounts.google.com/o/oauth2/token',
        authorize_url='https://accounts.google.com/o/oauth2/auth'
    )

    app.config["AUTH"] = google
    return google


def refresh_handler():
    oauth_resp = session.get("authorization")
    if oauth_resp is None or "refresh_token" not in oauth_resp:
        return False

    auth = current_app.config.get("AUTH")
    refresh_token = oauth_resp.get("refresh_token")

    data = {
        "client_id": current_app.config.get("GOOGLE_ID"),
        "client_secret": current_app.config.get("GOOGLE_SECRET"),
        "refresh_token": refresh_token,
        "grant_type": "refresh_token"
    }

    resp = auth.post('token', data=data)

    oauth_resp.update(resp)
    now = datetime.datetime.utcnow()
    expires_in = int(resp.get("expires_in", 3600))
    expires_at = now + datetime.timedelta(seconds=expires_in)
    oauth_resp.update(expires_at=calendar.timegm(expires_at.timetuple()))

    return now < expires_at
