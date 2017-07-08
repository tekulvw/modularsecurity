from google.appengine.ext import ndb
from .device import Device  # This is bad.


class System(ndb.Model):
    grace_period = ndb.IntegerProperty()
    alarm_count = ndb.IntegerProperty()
    ks_enabled = ndb.BooleanProperty(required=True)
    create_date = ndb.DateTimeProperty(auto_now_add=True)

    def to_json(self):
        sys_dict = self.to_dict()
        sys_dict['id'] = self.key.integer_id()

        devices = Device.from_system_key(self.key)
        sys_dict['devices'] = [d.to_json() for d in devices]
        return sys_dict


class Secondary(ndb.Model):
    oauth_id = ndb.StringProperty(required=True)
    system_id = ndb.StringProperty(required=True)
