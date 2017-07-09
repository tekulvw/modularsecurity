from google.appengine.ext import ndb


class Device(ndb.Model):
    serial_num = ndb.StringProperty()
    system_key = ndb.KeyProperty(kind="System")
    name = ndb.StringProperty()
    is_connected = ndb.BooleanProperty()
    device_type_key = ndb.IntegerProperty()

    @classmethod
    def from_serial_number(cls, serial_number):
        return cls.query(cls.serial_num == serial_number)

    @classmethod
    def from_system_key(cls, system_key):
        """
        Returns a list of devices associated with a given system key.
        :param system_key:
        :return:
        """
        dev_keys = cls.query(cls.system_key == system_key)
        count = dev_keys.count()
        if count > 0:
            return [d.get() for d in dev_keys.fetch(count)]
        return []

    def to_json(self):
        device_dict = self.to_dict(exclude=['system_key', 'device_type_key'])
        device_dict['system_id'] = self.system_key.integer_id()
        return device_dict


class DeviceData(ndb.Model):
    location = ndb.StringProperty()
    data_received = ndb.DateTimeProperty(auto_now_add=True)
    device_key = ndb.KeyProperty(kind="Device")

    def to_json(self):
        # TODO: serialize datetime
        data = {
            "location": self.location
        }
        return data

    @classmethod
    def create(cls, key):
        device_key = key

        return cls(
            device_key=device_key,
        )


class DeviceDataType(ndb.Model):
    type_name = ndb.StringProperty()

    def to_json(self):
        data = {
            "type_name": self.type_name
        }
        return data
