from google.appengine.ext import ndb

from .system import System
from .user import User


class Owner(ndb.Model):
    user_key = ndb.KeyProperty(kind="User")
    system_key = ndb.KeyProperty(kind="System")

    @classmethod
    def create(cls,oauth,grace):
        user_key = User.from_oauth_id(oauth)
        system_key = System.create(grace)
        return cls(
            user_key=user_key,
            system_key=system_key
        )


