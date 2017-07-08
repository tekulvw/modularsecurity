from google.appengine.ext import ndb


class Device(ndb.Model):
    serial_num = ndb.StringProperty()
    system_key = ndb.KeyProperty(kind="System")
    name = ndb.StringProperty()
    is_connected = ndb.BooleanProperty()
    device_type_key = ndb.IntegerProperty()

    def to_json(self):
        data={
            "serial_num": self.serial_num,
            "system_key": self.system_key,
            "name": self.name,
            "is_connected": self.is_connected,
            "device_type_key": self.device_type_key
        }
        return data

class DeviceData(ndb.Model):
    location = ndb.StringProperty()
    data_received = ndb.DateTimeProperty(auto_now_add=True)
    device_key = ndb.KeyProperty(kind="Device")
    grace_period = ndb.IntegerProperty()

    def to_json(self):
        data={
            "location": self.location,
            "data_received": self.data_received,
            "device_key": self.device_key,
            "grace_period": self.grace_period
        }
        return data
    def from_device_serial_number(cls,serial_number):
        return cls.query(cls.serial_num == serial_number)

    @classmethod
    def create(cls, key , data):
        location = data.get('location')
        data_received = data.get('data_received')
        device_key = key
        grace_period = data.get('grace_period')

        return cls(
            location=location,
            data_received=data_received,
            device_key=device_key,
            grace_period=grace_period
        )


class DeviceDataType(ndb.Model):
    type_name = ndb.StringProperty()

    def to_json(self):
        data={
            "type_name": self.type_name
        }
