from google.appengine.ext import ndb


class Owner(ndb.Model):
    user = ndb.KeyProperty(kind="User")
    system = ndb.KeyProperty(kind="System")
