from google.appengine.ext import ndb


class Owner(ndb.Model):
    user_key = ndb.KeyProperty(kind="User")
    system_key = ndb.KeyProperty(kind="System")
