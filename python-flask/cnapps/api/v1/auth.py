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

import flask
import flask_apispec
import flask_marshmallow
import marshmallow

from cnapps.api import commons
from cnapps.api.v1 import core
from cnapps.api.v1 import docs
from cnapps.middleware.auth import jwt
from cnapps.middleware.auth import request


REST = flask.Blueprint("auth", __name__)

LOGGER = logging.getLogger(__name__)

API_PATH = "/api/%s/auth" % core.PATH

MA = flask_marshmallow.Marshmallow()


class AuthenticationSchema(MA.Schema):

    userid = marshmallow.fields.Str()

    class Meta(object):
        strict = True


AUTHENT_SCHEMA = AuthenticationSchema()


@REST.route("%s/login" % API_PATH, methods=["POST"])
@flask_apispec.doc(
    description="Authenticate",
    params={
        request.USERNAME_HTTP_HEADER: docs.API_DOC_USER_KEY,
        request.PASSWORD_HTTP_HEADER: docs.API_DOC_PASSWORD_KEY,
    },
    responses={
        "200": {"description": "Success", "schema": AUTHENT_SCHEMA},
        "500": {"description": "If an unexpected error occurs"},
    },
    tags=[docs.API_DOC_AUTH],
)
@flask_apispec.marshal_with(AUTHENT_SCHEMA)
def api_auth_login():
    """Register a token.

    Returns:
        A HTTP response in JSON (application/json content-type)
    """

    LOGGER.info("Authenticate user")
    username, password = request.extract_credentials()
    user = flask.current_app.auth.authenticate_user(username, password)
    LOGGER.info("Credentials accepted for user: %s", user.name)
    roles = []
    user_roles = flask.current_app.auth.list_user_roles(user)
    for user_role in user_roles:
        LOGGER.debug("Search User role: %s", user_role)
        role = flask.current_app.auth.find_role(user_role.role['id'])
        LOGGER.info("User role: %s %s", roles, role)
        if role:
            roles.append(role)
    return commons.make_response(
        flask.jsonify(jwt.create_tokens(user, roles)), 200)
