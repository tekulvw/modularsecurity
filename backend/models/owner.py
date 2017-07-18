from google.appengine.ext import ndb

from models.system import System


class Owner(ndb.Model):
    user_key = ndb.KeyProperty(kind="User")
    system_key = ndb.KeyProperty(kind="System")

    @classmethod
    def create(cls, user_obj, grace):
        system = System.create(grace)
        system.put()
        return cls(
            user_key=user_obj.key,
            system_key=system.key
        )

    @classmethod
    def from_user(cls, user_obj):
        return cls.query(cls.user_key == user_obj.key).get()

    @classmethod
    def from_system(cls, system_obj):
        return cls.query(cls.system_key == system_obj.key).get()

    @staticmethod
    def is_owner_of(user, system):
        if system is None:
            return False

        owner = Owner.from_user(user)
        if owner is None:
            return False
        elif owner.system_key == system.key:
            return True
        return False

    def get_contact_number(self):
        user = self.user_key.get()
        if user:
            return user.phone_num
        return None
