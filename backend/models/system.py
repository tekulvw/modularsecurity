from google.appengine.ext import ndb


class System(ndb.Model):
    grace_period = ndb.IntegerProperty()
    alarm_count = ndb.IntegerProperty()
    ks_enabled = ndb.BooleanProperty(required=True)
    create_date = ndb.DateTimeProperty(auto_now_add=True)
