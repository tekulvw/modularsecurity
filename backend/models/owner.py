from google.appengine.ext import ndb

from .system import System
from .user import User


class Owner(ndb.Model):
    user_key = ndb.KeyProperty(kind="User")
    system_key = ndb.KeyProperty(kind="System")

    @classmethod
    def create(cls, oauth, grace):
        user = User.from_oauth_id(oauth)
        system = System.create(grace)
        system.put()
        return cls(
            user_key=user.key,
            system_key=system.key
        )

    @classmethod
    def from_user(cls, user_obj):
        return cls.query(cls.user_key == user_obj.key).get()
