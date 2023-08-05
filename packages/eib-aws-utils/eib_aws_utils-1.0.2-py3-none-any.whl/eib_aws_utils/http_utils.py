"""
    Copyright Engie Impact 2020.
    All rights reserved.
"""

__author__ = 'Engie Impact'

import requests
from requests.adapters import HTTPAdapter
from urllib3 import Retry


def create_requests_session(headers=None, api_gateway_key=None, max_retry=10, backoff_factor=1):
    """
    Create a requests session with custom retry policy.
    It will retry automatically if the http status code is 502, 503, 504.
    You can also provide some headers to be used or/and an API key.

    :param headers: the headers that must be used.
    :type headers: dict | None
    :param api_gateway_key: An api key that will be set in the "x-api-key" header.
      If set this value override the value in the "headers" parameter.
    :type api_gateway_key: str | None
    :param max_retry: Total number of retries to allow.
    :type max_retry: int | None
    :param backoff_factor: A backoff factor to apply between attempts after the second try.
      urllib3 will sleep for:: {backoff factor} * (2 ** ({number of total retries} - 1)) seconds.
      It will never be longer than 2 minutes.
    :type backoff_factor: float | None
    :return:
    :rtype:
    """
    session = requests.Session()

    retry_policy = Retry(
        total=max_retry,
        backoff_factor=backoff_factor,  # exponential managed by the number of retry
        status_forcelist=[502, 503, 504]
    )
    session.mount('https://', HTTPAdapter(max_retries=retry_policy))

    if headers:
        session.headers.update(headers)

    if api_gateway_key is not None:
        session.headers['x-api-key'] = api_gateway_key

    return session
