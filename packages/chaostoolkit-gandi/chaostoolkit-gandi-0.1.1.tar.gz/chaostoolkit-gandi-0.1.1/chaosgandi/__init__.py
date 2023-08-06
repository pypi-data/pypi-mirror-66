# -*- coding: utf-8 -*-
"""Top-level package for chaostoolkit-gandi."""
from contextlib import contextmanager
from urllib.parse import urljoin

from chaoslib.exceptions import ActivityFailed
from chaoslib.types import Configuration, Secrets
import requests

__all__ = ["gandi_client", "gandi_url"]
__version__ = '0.1.1'
GANDI_BASE_URL = "https://api.gandi.net"


@contextmanager
def gandi_client(configuration: Configuration,
                 secrets: Secrets) -> requests.Session:
    secrets = secrets or {}
    api_key = secrets.get("apikey")
    if not api_key:
        raise ActivityFailed(
            "You must provide the Gandi API key in the experiment secrets")

    headers = {
        "accept": "application/json",
        "content-type": "application/json; charset=utf-8",
        "Authorization": "Apikey {}".format(api_key.strip())
    }

    with requests.Session() as session:
        session.headers.update(headers)
        yield session


def gandi_url(path: str) -> str:
    return urljoin(GANDI_BASE_URL, path)
