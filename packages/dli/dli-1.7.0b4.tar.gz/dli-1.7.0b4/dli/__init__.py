import os
import warnings

warnings.filterwarnings(
    'always', module="dli"
)

__version__ = '1.7.0b4'


def connect(api_key=None,
            root_url="https://catalogue.datalake.ihsmarkit.com/__api",
            debug=None,
            strict=None):

    from dli.client.session import start_session

    return start_session(
        api_key,
        root_url=root_url,
        host=None,
        debug=debug,
        strict=strict
    )

def set_credentials(DLI_ACCESS_KEY_ID="", DLI_SECRET_ACCESS_KEY=""):
    if DLI_ACCESS_KEY_ID:
        os.environ["DLI_ACCESS_KEY_ID"] = DLI_ACCESS_KEY_ID

    if DLI_SECRET_ACCESS_KEY:
        os.environ["DLI_SECRET_ACCESS_KEY"] = DLI_SECRET_ACCESS_KEY
