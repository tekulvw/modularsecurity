import pytest

import sys
sys.path.insert(1, 'google_appengine')
sys.path.insert(1, 'google_appengine/lib/yaml/lib')
sys.path.insert(1, 'lib')


@pytest.fixture(autouse=True)
def init_datastore():
    from google.appengine.ext import testbed
    from google.appengine.ext import ndb

    # First, create an instance of the Testbed class.
    testbed = testbed.Testbed()
    # Then activate the testbed, which prepares the service stubs for use.
    testbed.activate()
    # Next, declare which service stubs you want to use.
    testbed.init_datastore_v3_stub()
    testbed.init_memcache_stub()
    # Clear ndb's in-context cache between tests.
    # This prevents data from leaking between tests.
    # Alternatively, you could disable caching by
    # using ndb.get_context().set_cache_policy(False)
    ndb.get_context().clear_cache()


@pytest.fixture(autouse=True)
def app():
    import main
    main.app.testing = True
    main.app.config['LOGIN_DISABLED'] = True
    app_client = main.app.test_client()

    return app_client


@pytest.fixture
def random_user():
    from models import User
    import uuid
    user = User(
        fname="FirstName",
        lname="LastName",
        phone_num=0000000000,
        oauth_id=str(uuid.uuid4())
    )
    user.put()
    yield user
    user.key.delete()


@pytest.fixture
def logged_in_app(app, random_user):
    with app.session_transaction() as sess:
        sess['user_id'] = random_user.oauth_id
        sess['_fresh'] = True
    return app
