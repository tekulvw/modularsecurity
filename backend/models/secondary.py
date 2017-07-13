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
