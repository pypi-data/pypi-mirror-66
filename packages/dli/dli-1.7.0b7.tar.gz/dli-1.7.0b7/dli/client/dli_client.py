import datetime
from json import JSONDecodeError
import warnings

import jwt
import requests
import logging
import socket
from http.cookiejar import CookiePolicy
from wrapt import ObjectProxy
from http import HTTPStatus
from urllib.parse import urljoin, urlparse, parse_qs
from collections import defaultdict
from dli import __version__
from dli.analytics import AnalyticsHandler
from dli.client.adapters import DLIBearerAuthAdapter, DLIAccountsV1Adapter, \
    DLIInterfaceV1Adapter, DLISamAdapter
from dli.client.components.urls import sam_urls, identity_urls
from dli.client.environments import _Environment
from dli.siren import siren_to_entity
from dli.client.components.auto_reg_metadata import AutoRegMetadata
from dli.client.components.datafile import Datafile
from dli.client.components.dataset import Dataset, Dictionary
from dli.client.components.me import Me
from dli.client.components.package import Package
from dli.client.components.search import Search
from dli.client.components.accounts import Accounts
from dli.client.exceptions import (
    DatalakeException, InsufficientPrivilegesException,
    InvalidPayloadException, UnAuthorisedAccessException,
    CatalogueEntityNotFoundException, AuthenticationFailure
)
from dli.models.paginator import Paginator
from dli.modules.dataset_module import DatasetModule
from dli.modules.package_module import PackageModule
from dli.models.dictionary_model import DictionaryModel
from dli.models.file_model import FileModel
from dli.models.instance_model import InstanceModel, \
    InstancesCollection as InstancesCollection_
from dli.models.package_model import PackageModel
from dli.models.dataset_model import DatasetModel
from dli.siren import PatchedSirenBuilder


class ModelDescriptor:
    """
    This class is responsible for extending the base type passed
    into the __init__ method with the instance of DliClient it has
    been created within, following the descriptor pattern.

    What this means practicably, is that under _client attribute of the 'new'
    type (class instance) there is a backreference to the DliClient,
    which then permits the type to access the shared session object of DliClient,
    rather than having to pass the session into each instance.

    Using an instance instantiated from the base type will not have the
    _client attribute available.
    """

    def __init__(self, model_cls=None):
        self.model_cls = model_cls

    def __get__(self, instance, owner):
        """Returns a model thats bound to the client instance"""
        return type(
            self.model_cls.__name__, (self.model_cls, ),
            {
                '_client': instance
            }
        )


class DliClient(Accounts, AutoRegMetadata,
                Datafile, Dataset, Dictionary,
                Me, Package, Search):
    """
    Definition of a client. This client mixes in utility functions for
    manipulating packages, datasets and datafiles.
    """

    Dataset = ModelDescriptor(DatasetModel)
    Instance = ModelDescriptor(InstanceModel)
    _InstancesCollection = ModelDescriptor(InstancesCollection_)
    _Pagination = ModelDescriptor(Paginator)
    _File = ModelDescriptor(FileModel)
    _Package = ModelDescriptor(PackageModel)
    _DictionaryV2 = ModelDescriptor(DictionaryModel)

    _packages = ModelDescriptor(PackageModule)
    _datasets = ModelDescriptor(DatasetModule)

    _environment_class = _Environment
    _session = None

    def __init__(self, api_root, host=None, debug=None, strict=True,
                 access_id=None, secret_key=None):
        self._environment = self._environment_class(api_root)
        self.access_id = access_id
        self.secret_key = secret_key
        self.host = host
        self.debug = debug
        self.strict = strict
        self.logger = logging.getLogger('global')
        self.logger.info(
            'Starting SDK session',
            extra={
               'catalogue': self._environment.catalogue,
               'consumption': self._environment.consumption,
               'strict' : strict,
               'version': __version__
            }
        )

        self._session = self._new_session()
        self._analytics_handler = AnalyticsHandler(self)

        self.packages = self._packages()
        self.datasets = self._datasets()

        if access_id is None and secret_key is not None:
            warnings.warn(
                'The parameter `api_key` will be deprecated in the future. '
                'We will be contacting users in the following months to '
                'explain how to migrate to the new authentication flow.',
                PendingDeprecationWarning
            )


    def _new_session(self):
        return Session(
            self.access_id,
            self.secret_key,
            self._environment,
            self.host,
            logger=self.logger
        )

    @property
    def session(self):
        # if the session expired, then reauth
        # and create a new context
        if self._session.has_expired:
            self._session = self._new_session()
        return self._session


class Session(requests.Session):

    def __init__(
        self, access_id, secret_key, environment, host, auth_key=None, logger=None
    ):
        super().__init__()
        self.logger = logger
        self.access_id = access_id
        self.secret_key = secret_key
        self._environment = environment
        self.host = host
        self.siren_builder = PatchedSirenBuilder()
        self._auth_init(auth_key)
        # mount points to add headers to specific routing requests
        self._set_mount_adapters()

        # Don't allow cookies to be set.
        # The new API will reject requests with both a cookie
        # and a auth header (as there's no predictable crediential to choose).
        #
        # However the old API, once authenticated using a Bearer token, will
        # as a side effect of a request return a oidc_id_token which matches
        # the auth header. This is ignored.
        self.cookies.set_policy(BlockAll())

    def _auth_init(self, auth_key=None):
        if not self.access_id:
            self.auth_key = auth_key or self._get_auth_key()
        else:
            self.auth_key = auth_key or self._get_SAM_auth_key()
        self.decoded_token = self._get_decoded_token()
        self.token_expires_on = self._get_expiration_date()


    def request(self, method, url, *args, **kwargs):
        if not urlparse(url).netloc:
            url = urljoin(self._environment.catalogue, url)

        kwargs.pop('hooks', None)
        hooks = {'response': self._response_hook}

        try:
            if self.logger:
                self.logger.debug(
                    'Request',
                    extra={
                        'method': method,
                        'request': url,
                        '-args': args,
                        '-kwargs': kwargs
                    }
                )

            return super().request(method, url, hooks=hooks, *args, **kwargs)
        except socket.error as e:
            raise ValueError(
                'Unable to process request due to a networking issue '
                'root cause could be a bad connection, '
                'not being on the correct VPN, '
                'or a network timeout '
            ) from e

    @property
    def has_expired(self):
        # We subtract timedelta from the expiration time in order to allow a safety window for
        # a code block to execute after a check has been asserted.
        return datetime.datetime.utcnow() > (self.token_expires_on - datetime.timedelta(minutes=1))

    def _response_hook(self, response, *args, **kwargs):
        # Apologies for the ugly code. The startswith siren check
        # is to make this only relevant to the old API.
        response = Response(response, self.siren_builder)

        if self.logger:
            self.logger.debug(
                'Response',
                extra={
                    # 'content': response.content,
                    'status': response.status_code,
                    'method': response.request.method,
                    'request': response.request.url,
                    'headers': response.request.headers
                }
            )

        if not response.ok:
            exceptions = defaultdict(
                lambda: DatalakeException,
                {HTTPStatus.BAD_REQUEST: InvalidPayloadException,
                 HTTPStatus.UNPROCESSABLE_ENTITY: InvalidPayloadException,
                 HTTPStatus.UNAUTHORIZED: UnAuthorisedAccessException,
                 HTTPStatus.FORBIDDEN: InsufficientPrivilegesException,
                 HTTPStatus.NOT_FOUND: CatalogueEntityNotFoundException}
            )

            try:
                message = response.json()
            except (JSONDecodeError, ValueError):
                message = response.text

            raise exceptions[response.status_code](
                message=message,
                params=parse_qs(urlparse(response.request.url).query),
                response=response
            )

        return response

    def _set_mount_adapters(self):
        self.mount(
            urljoin(self._environment.catalogue, '__api/'),
            DLIInterfaceV1Adapter(self)
        )

        self.mount(
            urljoin(self._environment.catalogue, '__api_v2/'),
            DLIBearerAuthAdapter(self)
        )

        self.mount(
            self._environment.consumption, DLIBearerAuthAdapter(self)
        )

        self.mount(
            urljoin(self._environment.accounts, 'api/identity/v1/'),
            DLIAccountsV1Adapter(self)
        )

        self.mount(
            urljoin(self._environment.accounts, 'api/identity/v2/'),
            DLIBearerAuthAdapter(self)
        )

        self.mount(
            self._environment.sam, DLISamAdapter(self)
        )

        self.mount(
            self._environment.consumption, DLIBearerAuthAdapter(self)
        )

    def _get_decoded_token(self):
        return jwt.decode(self.auth_key, verify=False)

    def _get_expiration_date(self):
        default_timeout = (
            datetime.datetime.utcnow() +
            datetime.timedelta(minutes=55)
        )

        if 'exp' not in self.decoded_token:
            return default_timeout

        return datetime.datetime.utcfromtimestamp(
            self.decoded_token['exp']
        ) - datetime.timedelta(minutes=5)

    def _get_auth_key(self):

        try:
            response = self.post(
                '/__api/start-session',
                headers={
                    'Authorization': 'Bearer {}'.format(
                        self.secret_key
                    )
                }
            )
        except DatalakeException as e:
            raise AuthenticationFailure(
                message='Could not authenticate API key'
            ) from e

        return response.text

    def _get_SAM_auth_key(self):

        sam_response = self.post(
            urljoin(self._environment.sam, sam_urls.sam_token),
            data={
                "client_id": self.access_id,
                "client_secret":  self.secret_key,
                "grant_type": "client_credentials"
            },
            hooks={'response': self._response_hook}
        )

        token = sam_response.json()["access_token"]

        catalogue_response = self.post(
            urljoin(self._environment.accounts,
                    identity_urls.identity_token),
            data={
                "client_id": self.access_id,
                "subject_token": token
            },
            hooks={'response': self._response_hook},
        )

        jwt = catalogue_response.json()["access_token"]
        return jwt


class Response(ObjectProxy):

    def __init__(self, wrapped, builder, *args, **kwargs):
        super(Response, self).__init__(wrapped, *args, **kwargs)
        self.builder = builder

    def to_siren(self):
        # Pypermedias terminology, not mine
        python_object = self.builder._construct_entity(
            self.json()
        ).as_python_object()

        # Keep the response availible
        python_object._raw_response = self

        return python_object

    def to_many_siren(self, relation):
        return [
            siren_to_entity(c) for c in
            self.to_siren().get_entities(rel=relation)
        ]


class BlockAll(CookiePolicy):
    return_ok = set_ok = domain_return_ok = path_return_ok = lambda self, *args, **kwargs: False
    netscape = True
    rfc2965 = hide_cookie2 = False
