import pytest
from mock import MagicMock
import sys

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
    app_client = main.app.test_client()

    import flask
    flask.current_app = app_client

    return app_client
