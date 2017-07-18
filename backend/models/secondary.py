from google.appengine.ext import ndb


class Secondary(ndb.Model):
    system_key = ndb.KeyProperty(kind="System")
    user_key = ndb.KeyProperty(kind="User")

    @classmethod
    def from_user(cls, user):
        """
        Returns a list of Secondaries from a given user.
        :param user: Datastore object
        :return: list of datastore objects
        """
        q = cls.query(cls.user_key == user.key)
        count = q.count()
        if count > 0:
            return q.fetch(count)
        return []

    @classmethod
    def create(cls, user, system):
        """
        Will not create duplicate secondary entries.
        :param user: User datastore object
        :param system: System datastore object
        :return: Secondary object
        """
        is_already_secondary, secondary = cls.is_secondary_of(user, system)
        if is_already_secondary:
            return secondary

        return cls(
            system_key=system.key,
            user_key=user.key
        )

    @classmethod
    def from_system_user(cls, system, user):
        """
        Tries to find a secondary entry from system and user objects
        :param system: Datastore object
        :param user: Datastore object
        :return: Secondary object or None
        """
        return cls.query(cls.system_key == system.key,
                         cls.user_key == user.key).get()

    @staticmethod
    def is_secondary_of(user, system):
        """
        Determines if a user is a secondary of a system.
        :param user: User datastore object
        :param system: System datastore object
        :return: bool, Secondary obj or None
        """
        q = Secondary.query(Secondary.system_key == system.key,
                            Secondary.user_key == user.key)
        secondary = q.get()
        return secondary is not None, secondary
