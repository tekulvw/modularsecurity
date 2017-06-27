from google.appengine.ext import ndb
from .device import Device  # This is bad.


class System(ndb.Model):
    VALID_UPDATE_ATTRS = ("grace_period", "alarm_count", "ks_enabled","create_date")
    grace_period = ndb.IntegerProperty()
    alarm_count = ndb.IntegerProperty()
    ks_enabled = ndb.BooleanProperty(required=True)
    create_date = ndb.DateTimeProperty(auto_now_add=True)

<<<<<<< HEAD
=======
    @classmethod
    def create(cls, grace):
        grace_period = grace
        return cls(
            grace_period=grace_period
        )

>>>>>>> 1633e94... Added resource file for system
    def to_json(self):
        sys_dict = self.to_dict()
        sys_dict['id'] = self.key.integer_id()

        devices = Device.from_system_key(self.key)
        sys_dict['devices'] = [d.to_json() for d in devices]
        return sys_dict

    @classmethod
    def create(cls,grace):
        grace_period = grace
        return cls(
            grace_period=grace_period
        )

    def update_from(self, data):
        """
        Updates this user with the given data. Data keys must be in
            VALID_UPDATE_ATTRS.
        :param data: dict
        :return:
        """
        if not self.valid_update_keys(data.keys):
            raise RuntimeError("Invalid update keys.")

        for k, v in data.items():
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


class Secondary(ndb.Model):
    oauth_id = ndb.StringProperty(required=True)
    system_id = ndb.StringProperty(required=True)
