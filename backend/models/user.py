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

    def get_id(self):
        return self.key


