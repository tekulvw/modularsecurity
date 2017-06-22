from google.appengine.ext import ndb
from flask_login import UserMixin

# Property Information can be found here:
# https://cloud.google.com/appengine/docs/standard/python/ndb/entity-property-reference


# noinspection PyUnresolvedReferences
class User(ndb.Model, UserMixin):
    fname = ndb.StringProperty()
    lname = ndb.StringProperty()
    phone_num = ndb.IntegerProperty()

    oauth_id = ndb.StringProperty(required=True)
    create_date = ndb.DateTimeProperty(auto_no_add=True)

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
        return self.key.integer_id()
