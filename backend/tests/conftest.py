import pytest
import sys

sys.path.insert(1, 'google_appengine')
sys.path.insert(1, 'google_appengine/lib/yaml/lib')
sys.path.insert(1, 'lib')

from models.device import Device, DeviceData
from models.system import System
from models.owner import Owner


@pytest.fixture(autouse=True)
def init_datastore():
    from google.appengine.ext import testbed
    from google.appengine.ext import ndb

    # First, create an instance of the Testbed class.
    testbed = testbed.Testbed()
    # Then activate the testbed, which prepares the service stubs for use.
    testbed.activate()
    # Next, declare which service stubs you want to use.
    testbed.init_app_identity_stub()
    testbed.init_datastore_v3_stub()
    testbed.init_memcache_stub()
    testbed.init_blobstore_stub()
    testbed.init_urlfetch_stub()
    # Clear ndb's in-context cache between tests.
    # This prevents data from leaking between tests.
    # Alternatively, you could disable caching by
    # using ndb.get_context().set_cache_policy(False)
    ndb.get_context().clear_cache()


@pytest.fixture(autouse=True)
def app(init_datastore):
    import main
    main.app.testing = True
    app_client = main.app.test_client()

    return app_client


@pytest.fixture
def user_factory(request):
    class UserFactory:
        def get(self):
            from models.user import User
            import uuid
            oauth_id = str(uuid.uuid4())
            user = User(
                fname="FirstName",
                lname="LastName",
                phone_num="0000000000",
                oauth_id=oauth_id,
                email="{}@email.com".format(oauth_id)
            )
            user.put()
            request.addfinalizer(user.key.delete)
            return user
    return UserFactory()


@pytest.fixture
def random_user(user_factory):
    return user_factory.get()


@pytest.fixture
def random_system():
    s = System.create(60)
    s.put()
    yield s
    s.key.delete()


@pytest.fixture
def random_owner(random_user, random_system):
    owner = Owner(user_key=random_user.key,
                  system_key=random_system.key)
    owner.put()
    yield owner
    owner.key.delete()


@pytest.fixture
def random_device_nosystem():
    dev = Device(
        serial_num="DEADBEEF"
    )
    dev.put()
    yield dev
    dev.key.delete()


@pytest.fixture
def random_device(random_device_nosystem, random_system):
    dev = random_device_nosystem
    dev.system_key = random_system.key
    dev.put()
    return dev


@pytest.fixture
def random_devicedata():
    data = DeviceData(
        location="Somewhere"
    )
    data.put()
    yield data
    data.key.delete()


@pytest.fixture
def logged_in_app(app, random_user):
    with app.session_transaction() as sess:
        sess['user_id'] = random_user.oauth_id
        sess['_fresh'] = True
    return app


@pytest.fixture
def admin_app(logged_in_app, random_user):
    random_user.is_admin = True
    random_user.put()
    return logged_in_app
