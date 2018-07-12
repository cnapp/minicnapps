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

from functools import wraps
import logging

from flask import request

from cnapps import exceptions
from cnapps.middleware.auth import jwt as jwt_auth
from cnapps.middleware.metrics import prometheus


LOGGER = logging.getLogger(__name__)

USERNAME_HTTP_HEADER = "X-USERNAME"

PASSWORD_HTTP_HEADER = "X-PASSWORD"

TOKEN_HTTP_HEADER = "Authorization"


def extract_credentials():
    # LOGGER.debug("Extract credentials from headers: %s", request.headers)
    if USERNAME_HTTP_HEADER not in request.headers:
        raise exceptions.UnauthorizedError("Invalid username")
    if PASSWORD_HTTP_HEADER not in request.headers:
        raise exceptions.UnauthorizedError("Invalid password")
    return request.headers[USERNAME_HTTP_HEADER], request.headers[
        PASSWORD_HTTP_HEADER]


def authenticate(role_name):
    """Extract user from HTTP headers and perform authentication

    Returns:
        user ([keystone.user]): the user find from Keystone

    Raises:
        exceptions.UnauthorizedError: if authentication headers are invalid or
            credentials are invalid
    """
    if request.headers is None:
        raise exceptions.UnauthorizedError()
    LOGGER.debug("Headers: {%s}", request.headers)

    if TOKEN_HTTP_HEADER in request.headers:
        jwt_auth.require_authentication_role(role_name)

    else:
        prometheus.API_USER.labels(request.path, 401, None).inc()
        raise exceptions.UnauthorizedError()


def admin_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        authenticate("admin")
        return f(*args, **kwargs)
    return wrap


def user_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        authenticate("user")
    return wrap
