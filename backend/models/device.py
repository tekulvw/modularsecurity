from google.appengine.ext import ndb


class Device(ndb.Model):
    serial_num = ndb.StringProperty()
    system_key = ndb.KeyProperty(kind="System")
    name = ndb.StringProperty()
    is_connected = ndb.BooleanProperty()
    device_type_key = ndb.IntegerProperty()


class DeviceData(ndb.Model):
    location = ndb.StringProperty()
    data_received = ndb.DateTimeProperty(auto_now_add=True)
    device_key = ndb.KeyProperty(kind="Device")
    grace_period = ndb.IntegerProperty()


class DeviceDataType(ndb.Model):
    type_name = ndb.StringProperty()
