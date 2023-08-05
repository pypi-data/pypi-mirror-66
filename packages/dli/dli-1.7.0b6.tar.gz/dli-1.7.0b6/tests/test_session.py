import os
from unittest import mock

import pytest
import unittest
import jwt

from unittest.mock import MagicMock
import httpretty

from dli import __version__, set_credentials
from dli.client.dli_client import Session, DliClient
from dli.client.session import start_session
from dli.client import session
from dli.client.exceptions import (
    DatalakeException,
    InsufficientPrivilegesException,
    UnAuthorisedAccessException
)
from dli.siren import PatchedSirenBuilder

environ = MagicMock(catalogue='http://catalogue.local',
                    accounts='')
valid_token = jwt.encode({"exp": 9999999999}, 'secret')
expired_token = jwt.encode({"exp": 1111111111}, 'secret')

class SessionTestCase(unittest.TestCase):

    def test_can_decode_valid_jwt_token(self):
        ctx = Session(
            None,
            "key",
            environ,
            None,
            valid_token
        )

        self.assertFalse(ctx.has_expired)

    def test_can_detect_token_is_expired(self):
        ctx = Session(
            None,
            "key",
            environ,
            None,
            expired_token
        )
        self.assertTrue(ctx.has_expired)


class SessionRequestFactoryTestCase(unittest.TestCase):

    @pytest.fixture(autouse=True)
    def session(self):
        self.session = Session(None, None, environ, None, valid_token)

    @httpretty.activate
    def test_response_403_raises_InsufficientPrivilegesException(self):
        response_text = 'Insufficient Privileges'
        httpretty.register_uri(
            httpretty.GET, 'http://catalogue.local/test',
            status=403, body=response_text
        )

        with self.assertRaises(InsufficientPrivilegesException):
            self.session.get('/test')

    @httpretty.activate
    def test_response_401_raises_UnAuthorisedAccessException(self):
        response_text = 'UnAuthorised Access'
        httpretty.register_uri(
            httpretty.GET, 'http://catalogue.local/test',
            status=401, body=response_text
        )


        with self.assertRaises(UnAuthorisedAccessException):
            self.session.get('/test')

    @httpretty.activate
    def test_response_500_raises_DatalakeException(self):
        response_text = 'Datalake server error'
        httpretty.register_uri(
            httpretty.GET, 'http://catalogue.local/test',
            status=500, body=response_text
        )

        with self.assertRaises(DatalakeException):
            self.session.get('/test')

    @httpretty.activate
    def test_sdk_version_is_included_in_header(self):
        httpretty.register_uri(
            httpretty.GET, 'http://catalogue.local/__api/',
            status=200, body="response"
        )
        # issue a request
        self.session.get('/__api/')

        request = httpretty.last_request()
        self.assertTrue("X-Data-Lake-SDK-Version" in request.headers)
        self.assertEqual(request.headers["X-Data-Lake-SDK-Version"], str(__version__))


class TestEnv:
    sam = "Test"
    catalogue = "Test"
    accounts = "Test"


class TestSessionMock(Session):

    def __init__(self, id, pasw):
        self._get_SAM_auth_key = MagicMock()
        self._get_auth_key = MagicMock()
        self._get_decoded_token = MagicMock()
        self._get_expiration_date = MagicMock()
        self._set_mount_adapters = MagicMock()
        super().__init__(id, pasw, {}, "Test")


class TestClientMock(DliClient):

    def __init__(self, api_root, host=None, debug=None, strict=True,
                 access_id=None, secret_key=None):
        super().__init__("Test", access_id=access_id, secret_key=secret_key)

    def _new_session(self):
        return TestSessionMock("Test", "Test")


class TestSessionMockWithAuth(Session):

    def __init__(self, id, pasw):
        self._set_mount_adapters = MagicMock()
        self.access_id = id
        self.secret_key = pasw
        self.auth_key = None
        self._environment = TestEnv()
        self.host = None
        self.siren_builder = PatchedSirenBuilder()


class TestClientMockWithAuth(TestClientMock):

    def _new_session(self):
        return TestSessionMockWithAuth(self.access_id, self.secret_key)


@pytest.fixture
def test_session():
    yield TestSessionMock


@pytest.fixture
def mock_del_env_user(monkeypatch):
    monkeypatch.delenv("DLI_ACCESS_KEY_ID", raising=False)
    monkeypatch.delenv("DLI_SECRET_ACCESS_KEY", raising=False)


@pytest.fixture
def mock_create_env_user(monkeypatch):
    monkeypatch.setenv("DLI_ACCESS_KEY_ID", "TestingUser")
    monkeypatch.setenv("DLI_SECRET_ACCESS_KEY", "TestingPass")

def test_credential_helper():
    set_credentials("test-access-id", "test-access-key")
    assert(os.environ["DLI_ACCESS_KEY_ID"] == "test-access-id")
    assert(os.environ["DLI_SECRET_ACCESS_KEY"] == "test-access-key")


def test_credentials_no_api_key(monkeypatch, mock_create_env_user, recwarn):
    # test flow when u/p set and no api key set
    monkeypatch.setattr(DliClient, '_new_session', lambda x: x)
    dl = start_session()
    assert(issubclass(type(dl), DliClient))
    assert len(recwarn) == 0
    assert(dl.secret_key is not None and dl.access_id is not None)


def test_credentials_session(mock_create_env_user, test_session):
    # test flow when u/p set and no api key set

    sesh = test_session(os.environ["DLI_ACCESS_KEY_ID"],
                        os.environ["DLI_SECRET_ACCESS_KEY"])
    assert sesh._get_SAM_auth_key.call_count == 1


def test_api_key_deprecation_warning(recwarn, monkeypatch):
    # test flow when u/p set and api key set
    # api key should override
    monkeypatch.setattr(DliClient, '_new_session', MagicMock())
    dl = start_session(api_key="Test")
    assert(issubclass(type(dl), DliClient))
    assert len(recwarn) == 1
    assert(dl.secret_key is not None and dl.access_id is None)


def test_credentials_and_api_key(mock_create_env_user, monkeypatch):
    # test flow when u/p set and api key set
    # api key should override
    monkeypatch.setattr(DliClient, '_new_session',  MagicMock())
    dl = start_session(api_key="Test")
    assert (dl.secret_key is not None and dl.access_id is None)


def test_api_session(mock_create_env_user, test_session):
    # test flow when u/p set and no api key set
    # (there will be no acces id set)
    sesh = test_session(None, "Test")
    assert sesh._get_auth_key.call_count == 1


def test_credentials_and_no_api_key(mock_create_env_user, monkeypatch, caplog):
    # test flow when no credentials and api key set
    monkeypatch.setattr(session, "get_client", lambda: TestClientMock)
    dl = start_session()
    for x in caplog.records:
        assert("old" not in x.message)


def test_no_credentials_and_api_key(mock_del_env_user, monkeypatch, caplog):
    # test flow when no credentials and api key set
    monkeypatch.setattr(session, "get_client", lambda: TestClientMock)
    dl = start_session(api_key="Test")
    assert (dl.secret_key is not None and dl.access_id is None)
    for x in caplog.records:
        assert("new" not in x.message)


def test_api_key_auth(mock_del_env_user, monkeypatch):
    # test old auth process (_get_auth_key())
    api_response = valid_token
    monkeypatch.setattr(session, "get_client", lambda: TestClientMockWithAuth)
    dl = start_session(api_key="API")
    dl._session.post = MagicMock()
    dl._session.post.return_value.text = api_response

    dl._session._auth_init()
    assert(dl and dl._session.auth_key is not None)


def test_credentials_auth(mock_create_env_user, monkeypatch):
    # test new auth process (_get_SAM_auth_key())
    sam_response = {
        "access_token": valid_token,
        "token_type": "Bearer", "expires_in": 3599}
    catalogue_response = {
        "access_token": valid_token,
        "token_type": "Bearer", "expires_in": 3599}

    monkeypatch.setattr(session, "get_client", lambda: TestClientMockWithAuth)
    dl = start_session()
    dl._session.post = MagicMock()
    dl._session.post.return_value.json.side_effect = [
        sam_response, catalogue_response
    ]

    dl._session._auth_init()
    assert(dl and dl._session.auth_key is not None)


@pytest.mark.xfail
def test_SAM_flow(mock_del_env_user, monkeypatch, caplog):
    # test flow when no credentials and api key set
    monkeypatch.setattr(session, "get_client", lambda: TestClientMock)
    dl = start_session()
    for x in caplog.records:
        assert("new" not in x.message)
        assert ("old" not in x.message)

    # not implemented
    # we should get a dl back after the SAM flow is implemented
    assert (dl.secret_key is not None and dl.access_id is None)


@pytest.fixture
def real_client(request):
    # This is the S3 address used for the QA environment.
    api_root = os.environ[f'{request.param[0]}_API_URL']
    accessid = os.environ[f'{request.param[0]}_ACCESS_ID']
    secretkey = os.environ[f'{request.param[0]}_SECRET_ACCESS_KEY']
    client = None

    if request.param[1] == "Credentials":
        client = DliClient(
            api_root=api_root,
            access_id=accessid,
            secret_key=secretkey
        )
    elif request.param == 'API':
        pass
    else:
        pass

    yield client


@pytest.mark.xfail
@pytest.mark.integration
@pytest.mark.parametrize('real_client', [('QA', "Credentials")],
                         indirect=['real_client'])
def test_credentials_on_catalogue(real_client):
    # test that new auth actually works and returns JWT
    assert(real_client.session._get_auth_key() is not None)
    assert(real_client.datasets._get(
        "autotestdatasetItsdeclarationRomanZimmermannandpeople"
    ) is not None)
