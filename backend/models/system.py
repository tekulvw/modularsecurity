from google.appengine.ext import ndb
from .device import Device  # This is bad.
from models.device import DeviceData


class System(ndb.Model):
    VALID_UPDATE_ATTRS = ("name", "grace_period", "alarm_count", "ks_enabled","create_date")

    name = ndb.StringProperty(default="Default")
    grace_period = ndb.IntegerProperty()
    alarm_count = ndb.IntegerProperty()
    ks_enabled = ndb.BooleanProperty(required=True)
    create_date = ndb.DateTimeProperty(auto_now_add=True)

    @classmethod
    def create(cls, grace):
        grace_period = grace
        return cls(
            grace_period=grace_period,
            ks_enabled=False
        )

    @classmethod
    def from_system_id(cls, system_id):
        if system_id:
            return ndb.Key(cls, system_id).get()
        return None

    def to_json(self):
        sys_dict = self.to_dict(exclude=['create_date', ])
        sys_dict['id'] = self.key.integer_id()

        devices = Device.from_system_key(self.key)
        sys_dict['devices'] = [d.to_json() for d in devices]
        return sys_dict

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
            if k == "grace_period":
                v = int(v)
            if k == "grace_period" and v < 0:
                raise ValueError("Grace Period must be 0 or greater")
            if k == "name" and len(v) * 4 >= 1500:
                raise ValueError("System name is too big!")
            setattr(self, k, v)

        self.put()

    @staticmethod
    def valid_update_keys(keys):
        """
        Determines if the given list of keys are valid attributes.

        Used in conjunction with resources/user/User/update
        :param keys: list[str]
        :return: bool
        """
        for k in keys:
            if k not in System.VALID_UPDATE_ATTRS:
                return False
        return True

    def get_latest_data_frames(self):
        """
        Gets the most recent DeviceData frames from all connected devices.
        :return:
        """
        devices = Device.from_system_key(self.key)
        frames = [f for d in devices for f in DeviceData.get_last(d)]
        return frames
