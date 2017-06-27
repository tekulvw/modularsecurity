from google.appengine.ext import ndb


class Secondary(ndb.Model):
    system_key = ndb.KeyProperty(kind="System")
    user_key = ndb.KeyProperty(kind="User")