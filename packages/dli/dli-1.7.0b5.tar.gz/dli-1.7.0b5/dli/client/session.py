import logging
import os
import warnings

from dli.client import _setup_logging
from dli.client.dli_client import DliClient
from dli import __version__
import requests

DEPRECATED_AGE = 1


def version_check(package_name):
    url = f"https://pypi.python.org/pypi/{package_name}/json"

    try:
        data = requests.get(url).json()
        versions = list(x for x in data["releases"].keys() if 'b' not in x)
        versions = sorted(versions)
        versions.reverse()

        offset = versions.index(__version__)

        if offset > DEPRECATED_AGE:
            warnings.warn("You are using an old version of the SDK, please upgrade"
                          "using `pip install [dli] --upgrade` "
                          "before the SDK no longer functions as expected",
                          PendingDeprecationWarning)
    except:
        # Version check has been see to fail by Gilberto with an SSLError
        # when doing the handshake with pypi.
        pass


class PEBCAKWarning(UserWarning):
    pass


def start_session(
    api_key=None,
    root_url="https://catalogue.datalake.ihsmarkit.com/__api",
    host=None,
    debug=False,
    strict=True,
):
    """
    Entry point for the Data Lake SDK, returns a client instance that
    can be used to consume or register datasets.

    Example for starting a session:

        from dli.client import session
        dl = session.start_session(api_key)

    :param str api_key: Your API key, can be retrieved from your dashboard in
                        the Catalogue UI.
    :param str root_url: Optional. The environment you want to point to. By default it
                        points to Production.
    :param str host: Optional. Advanced usage, meant to force a hostname when DNS resolution
                     is not reacheable from the user's network.
                     This is meant to be used in conjunction with an
                     IP address as the root url.
                     Example: catalogue.datalake.ihsmarkit.com

    :param bool debug: Optional. Log SDK operations to a file in the current working
                       directory with the format "sdk-{end of api key}-{timestamp}.log"

    :param bool strict: Optional. When True, all exception messages and stack
                        trace are printed. When False, a shorter message is
                        printed and `None` should be returned.

    :returns: Data Lake interface client
    :rtype: dli.client.dli_client.DliClient

    """
    logger = _setup_logging(debug)
    version_check('dli')

    user = os.environ.get("DLI_ACCESS_KEY_ID")
    pasw = os.environ.get("DLI_SECRET_ACCESS_KEY")
    api_key = api_key or os.environ.get("DLI_API_KEY")

    logger.debug("Checking auth flow")

    if (user is not None and pasw is not None) and api_key is None:
        logger.debug("Using new application authentication flow")
        return get_client()(root_url, host, debug=debug, strict=strict,
                            access_id=user, secret_key=pasw)
    elif (user is None or pasw is None) and api_key is None:
        logger.debug("Using SAM application authentication flow")
        url = "test"
        print(f"If your browser has not been automatically opened, "
              f"then please copy and paste this URL into your browser "
              f"to complete the login process within the next 15 minutes:\n"
              f"{url}")

        return
    elif api_key is not None:
        logger.debug("Using old application authentication flow")
        if api_key is not None:
            return get_client()(root_url, host, debug=debug, strict=strict,
                                secret_key=api_key)

def get_client():
    return DliClient
