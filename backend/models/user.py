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
    phone_num = ndb.IntegerProperty()

    is_admin = ndb.BooleanProperty(default=False)

    oauth_id = ndb.StringProperty(required=True)
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

        return cls(
            fname=fname,
            lname=lname,
            oauth_id=oauth_id
        )

    @classmethod
    def from_oauth_id(cls, oauth_id):
        """
        Retrieves a user based on the given oauth_id.
        :param oauth_id:
        :return: User, None
        """
        return cls.query(cls.oauth_id == oauth_id).get()

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
            setattr(self, k, v)

        self.put()

    def to_json(self):
        data = {
            "fname": self.fname,
            "lname": self.lname,
            "phone_num": self.phone_num,
            "owned_systems": self.owned_systems(),
            "secondary_systems": self.secondary_systems()
        }
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

    def owned_systems(self):
        q = ndb.Query(kind="Owner")
        q.filter(ndb.GenericProperty("user_key") == self.key)
        count = q.count()

        owned = []
        if count > 0:
            owned = [o.system_key.get() for o in q.fetch(count)]

        return [s.to_json() for s in owned]

    def secondary_systems(self):
        q = ndb.Query(kind="Secondary")
        q.filter(ndb.GenericProperty("user_key") == self.key)
        count = q.count()

        secondary = []
        if count > 0:
            secondary = [s.system_key.get() for s in q.fetch(count)]

        return [s.to_json() for s in secondary]

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
