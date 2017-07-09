from google.appengine.ext import ndb

from models.system import System as SystemModel
from models.user import User as UserModel


class Owner(ndb.Model):
    user_key = ndb.KeyProperty(kind="User")
    system_key = ndb.KeyProperty(kind="System")

    @classmethod
    def create(cls,oauth,grace):
        user_key = UserModel.User.from_oauth_id(oauth)
        system_key = SystemModel.System.create(grace)
        return cls(
            user_key=user_key,
            system_key=system_key
        )


