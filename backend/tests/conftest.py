import pytest
from mock import MagicMock
import sys

import sys
sys.path.insert(1, 'google_appengine')
sys.path.insert(1, 'google_appengine/lib/yaml/lib')
sys.path.insert(1, 'lib')


@pytest.fixture
def app():
    import main
    main.app.testing = True
    return main.app.test_client()
