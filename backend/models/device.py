from google.appengine.ext import ndb


class Device(ndb.Model):
    enabled = ndb.BooleanProperty(default=True)
    serial_num = ndb.StringProperty()
    system_key = ndb.KeyProperty(kind="System")
    name = ndb.StringProperty(default="Default Device")
    is_connected = ndb.BooleanProperty()
    device_type_key = ndb.KeyProperty(kind="DeviceDataType")

    @classmethod
    def create(cls, serial_number, type_=None):
        """
        Create a new unassociated device in the datastore.
        :param serial_number: Device serial number
        :param type_: DeviceDataType instance or None
        :return:
        """
        type_ = type_ or DeviceDataType.default_type()
        return cls(
            serial_num=serial_number,
            device_type_key=type_.key
        )

    @classmethod
    def from_serial_number(cls, serial_number):
        return cls.query(cls.serial_num == serial_number).get()

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
            return dev_keys.fetch(count)
        return []

    def to_json(self):
        device_dict = self.to_dict(exclude=['system_key', 'device_type_key'])
        if self.system_key:
            device_dict['system_id'] = self.system_key.integer_id()
        else:
            device_dict['system_id'] = None
        return device_dict

    def update_type(self, data_type):
        """
        Maybe updates the devices data type based on the given DeviceDataType
            object.
        :param data_type:
        :return:
        """
        # If we ever allow single Pi's to have multiple sensors we must put
        # this information into DeviceData which, tbh, makes sense to have
        # there now but oh well.
        if self.device_type_key != data_type.key:
            self.device_type_key = data_type.key
            self.put()

    def update_from(self, data):
        """
        Updates this user with the given data. Data keys must be in
            VALID_UPDATE_ATTRS.
        :param data: dict
        :return:
        """
        if not self.valid_update_keys(data.keys()):
            raise RuntimeError("Invalid update keys.")

        for k, v in data.items():
            setattr(self, k, v)

        self.put()

    def valid_update_keys(self, keys):
        """
        Determines if the given list of keys are valid attributes.

        Used in conjunction with resources/user/User/update
        :param keys: list[str]
        :return: bool
        """
        valid_keys = self.to_dict(exclude=["system_key", "device_type_key",
                                           "is_connected", "serial_num"]).keys()
        for k in keys:
            if k not in valid_keys:
                return False
        return True


class DeviceData(ndb.Model):
    location = ndb.StringProperty()
    data_received = ndb.DateTimeProperty(auto_now_add=True)
    device_key = ndb.KeyProperty(kind="Device")

    def to_json(self):
        # TODO: serialize datetime
        device = self.device_key.get()
        try:
            system_id = device.system_key.integer_id()
        except AttributeError:
            system_id = None

        data = {
            "location": self.location,
            "system_id": system_id,
            "device_id": self.device_key.integer_id()
        }

        return data

    @classmethod
    def create(cls, key):
        device_key = key

        return cls(
            device_key=device_key,
        )

    @classmethod
    def from_device(cls, device):
        """
        Gets all data entries from the given device.
        :param device: datastore object
        :return: list
        """
        q = cls.query(cls.device_key == device.key)
        count = q.count()
        if count > 0:
            return q.fetch(count)
        return []

    @classmethod
    def get_last(cls, device, n=1):
        """
        Gets last n data frames from given device.
        :param device:
        :param n:
        :return:
        """
        q = cls.query(cls.device_key == device.key)
        # noinspection PyUnresolvedReferences
        q = q.order(-cls.data_received)
        count = min(n, q.count())
        if count > 0:
            return q.fetch(count)
        return []


class DeviceDataType(ndb.Model):
    type_name = ndb.StringProperty()
    is_binary = ndb.BooleanProperty(required=True)

    mime_type = ndb.StringProperty(required=True)

    def to_json(self):
        # type: () -> dict
        data = self.to_dict()
        return data

    @classmethod
    def default_type(cls):
        default = cls.from_name("default")
        if default is None:
            default = DeviceDataType(
                type_name="default",
                is_binary=False,
                mime_type="application/json"
            )
            default.put()
        return default

    @classmethod
    def from_name(cls, type_name):
        """
        Gets Data Type object from the given name.
        :param type_name:
        :return: Datastore object or None
        """
        return cls.query(cls.type_name == type_name).get()
