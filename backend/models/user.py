from google.appengine.ext import ndb
from flask import session, current_app
from flask_login import UserMixin
import datetime
import os


# Property Information can be found here:
# https://cloud.google.com/appengine/docs/standard/python/ndb/entity-property-reference


# noinspection PyUnresolvedReferences
class User(ndb.Model, UserMixin):
    VALID_UPDATE_ATTRS = ("fname", "lname", "phone_num")

    fname = ndb.StringProperty()
    lname = ndb.StringProperty()
    phone_num = ndb.StringProperty()

    is_admin = ndb.BooleanProperty(default=False)

    oauth_id = ndb.StringProperty(required=True)
    email = ndb.StringProperty(required=True)
    create_date = ndb.DateTimeProperty(auto_now_add=True)

    @classmethod
    def create(cls, userinfo):
        """
        Creates a user from the given userinfo object.
        :param userinfo: result of auth.get('userinfo')
        :return:
        """
        data = userinfo.data
        fname = data.get("given_name", "")
        lname = data.get("family_name", "")
        oauth_id = data.get("id", "")
        email = data.get("email", "")

        return cls(
            fname=fname,
            lname=lname,
            oauth_id=oauth_id,
            email=email
        )

    @classmethod
    def from_oauth_id(cls, oauth_id):
        """
        Retrieves a user based on the given oauth_id.
        :param oauth_id:
        :return: User, None
        """
        return cls.query(cls.oauth_id == oauth_id).get()

    @classmethod
    def from_email(cls, email_addr):
        """
        Finds a user from the given email address
        :param email_addr:
        :return: User object or None
        """
        return cls.query(cls.email == email_addr).get()

    def update_from(self, data):
        """
        Updates this user with the given data. Data keys must be in
            VALID_UPDATE_ATTRS.
        :param data: dict
        :return:
        """
        if not self.valid_update_keys(data.keys()):
            raise RuntimeError("Invalid update keys.")

        for k, v in data.items():
            if k == "phone_num" and v is None:
                raise ValueError("Phone number is empty")
            if k == "phone_num" and len(v) != 10:
                raise ValueError("Phone number too long or short!")
            if k == "phone_num" and v.isdigit() is False:
                raise ValueError("Phone number must be a number!")
            setattr(self, k, v)
        self.put()

    def to_json(self):
        data = self.to_dict(exclude=["create_date"])
        return data

    def get_id(self):
        return self.oauth_id

    @property
    def is_authenticated(self):
        if os.environ.get("TESTING"):
            return True

        oauth_resp = session.get("authorization")
        if oauth_resp is None:
            return False

        now = datetime.datetime.utcnow()
        expires_at = datetime.datetime.utcfromtimestamp(oauth_resp["expires_at"])
        if now > expires_at:
            login_manager = current_app.config.get("LOGIN_MGR")
            return login_manager.needs_refresh()
        return True

    @staticmethod
    def valid_update_keys(keys):
        """
        Determines if the given list of keys are valid attributes.

        Used in conjunction with resources/user/User/update
        :param keys: list[str]
        :return: bool
        """
        for k in keys:
            if k not in User.VALID_UPDATE_ATTRS:
                return False
        return True
