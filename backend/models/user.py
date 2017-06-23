from google.appengine.ext import ndb
from flask import session, current_app
from flask_login import UserMixin
import datetime

# Property Information can be found here:
# https://cloud.google.com/appengine/docs/standard/python/ndb/entity-property-reference


# noinspection PyUnresolvedReferences
class User(ndb.Model, UserMixin):
    fname = ndb.StringProperty()
    lname = ndb.StringProperty()
    phone_num = ndb.IntegerProperty()

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

    def get_id(self):
        return self.oauth_id

    @property
    def is_authenticated(self):
        oauth_resp = session.get("authorization")
        if oauth_resp is None:
            return False

        now = datetime.datetime.utcnow()
        expires_at = datetime.datetime.utcfromtimestamp(oauth_resp["expires_at"])
        if now > expires_at:
            login_manager = current_app.config.get("LOGIN_MGR")
            return login_manager.needs_refresh()
        return True
