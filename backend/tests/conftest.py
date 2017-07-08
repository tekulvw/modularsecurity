import pytest
from mock import MagicMock
import sys


@pytest.fixture(autouse=True)
def patch_ndb(monkeypatch):
    sys.modules['google'] = MagicMock()
    sys.modules['google.appengine'] = MagicMock()
    model_mock = MagicMock()
    model_mock.ndb.Model = type('EmptyTypeThing', (object, ), {})
    sys.modules['google.appengine.ext'] = model_mock
    yield
    del sys.modules['google']
    del sys.modules['google.appengine']
    del sys.modules['google.appengine.ext']


@pytest.fixture
def app():
    import main
    main.app.testing = True
    return main.app.test_client()