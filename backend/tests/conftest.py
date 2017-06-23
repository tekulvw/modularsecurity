import pytest
from mock import MagicMock


@pytest.fixture(autouse=True)
def patch_ndb(monkeypatch):
    monkeypatch.setattr('google.appengine.ext.ndb', MagicMock)