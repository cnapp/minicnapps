# Copyright (C) 2018 Nicolas Lamirault <nicolas.lamirault@gmail.com>

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import logging

LOGGER = logging.getLogger(__name__)


def _get_content_type_json():
    return "application/json"


def _get_headers():
    headers = {}
    headers["Content-Type"] = _get_content_type_json()
    return headers


def get(app_client, uri, headers=None):
    """Perform a HTTP GET request

    Args:
        app_client ([flask.app.http_client]): the HTTP client from the Test
            application
        uri ([string]): the URL request
        headers ([dict], optional): Defaults to None. HTTP headers to send

    Returns:
        [type]: the HTTP response
    """
    if not headers:
        headers = _get_headers()
    LOGGER.info("GET : %s %s", uri, headers)
    return app_client.get(uri, headers=headers, follow_redirects=True)


def post(app_client, uri, data=dict(), headers=None):
    """Perform a HTTP POST request

    Args:
        app_client ([flask.app.http_client]): the HTTP client from the Test
            application
        uri ([string]): the URL request
        data ([dict, optional]): the parameters to send
        headers ([dict], optional): Defaults to None. HTTP headers to send

    Returns:
        [type]: the HTTP response
    """
    content_type = _get_content_type_json()
    if not headers:
        headers = _get_headers()
    LOGGER.info("POST : %s %s %s", uri, data, headers)
    return app_client.post(
        uri,
        headers=headers,
        data=data,
        content_type=content_type,
        follow_redirects=True,
    )


def put(app_client, uri, data=dict(), headers=None):
    """Perform a HTTP PUT request

    Args:
        app_client ([flask.app.http_client]): the HTTP client from the Test
            application
        uri ([string]): the URL request
        data ([dict, optional]): the parameters to send
        headers ([dict], optional): Defaults to None. HTTP headers to send

    Returns:
        [type]: the HTTP response
    """
    content_type = _get_content_type_json()
    if not headers:
        headers = _get_headers()
    LOGGER.info("PUT : %s %s %s", uri, data, headers)
    return app_client.put(
        uri,
        data=data,
        headers=headers,
        content_type=content_type,
        follow_redirects=True,
    )


def delete(app_client, uri, headers=None):
    """Perform a HTTP DELETE request

    Args:
        app_client ([flask.app.http_client]): the HTTP client from the Test
            application
        uri ([string]): the URL request
        headers ([dict], optional): Defaults to None. HTTP headers to send

    Returns:
        [type]: the HTTP response
    """
    content_type = _get_content_type_json()
    if not headers:
        headers = _get_headers()
    LOGGER.info("DELETE: %s %s", uri, headers)
    return app_client.delete(
        uri, headers=headers, content_type=content_type, follow_redirects=True
    )
