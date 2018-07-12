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

import datetime
import logging

import flask_jwt_extended
from flask_jwt_extended import exceptions as jwt_exc

from cnapps import exceptions


LOGGER = logging.getLogger(__name__)

JWT_MANAGER = flask_jwt_extended.JWTManager()


def setup(app):
    """Setup JWT

    Args:
        app ([flask.Flask]): the main application
    """

    JWT_MANAGER.init_app(app)
    app.config['JWT_SECRET_KEY'] = "my-secret"
    app.config['JWT_TOKEN_LOCATION'] = ['headers']
    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = datetime.timedelta(hours=1)


def create_tokens(user, roles):
    user_roles = []
    for role in roles:
        user_roles.append(role.name)
    LOGGER.info("User: %s Roles: %s", user, user_roles)
    identity = {
        'userid': user.id,
        'roles': user_roles,
    }
    return {
        'access_token': flask_jwt_extended.create_access_token(identity),
        'refresh_token': flask_jwt_extended.create_refresh_token(identity),
    }


def require_authentication_role(role_name):
    try:
        flask_jwt_extended.verify_jwt_in_request()
        identity = flask_jwt_extended.get_jwt_identity()
        LOGGER.info("Identity: %s Role: %s", identity, role_name)
        if role_name not in identity['roles']:
            raise exceptions.ForbiddenError(
                "Access forbidden for user %s" % identity
            )
        LOGGER.info("User %s have role: %s", identity, role_name)

    except jwt_exc.JWTExtendedException as err:
        raise exceptions.JWTError(str(err), 401)


@JWT_MANAGER.user_loader_error_loader
def custom_user_loader_error(identity):
    LOGGER.warning("Invalid user: %s", identity)
    raise exceptions.JWTError("User {} not found".format(identity), 404)


@JWT_MANAGER.expired_token_loader
def expired_token_callback():
    raise exceptions.JWTError("Token has expired", 401)


@JWT_MANAGER.invalid_token_loader
def invalid_token_callback(error):
    raise exceptions.JWTError(
        "Signature verification failed: %s" % str(error), 401)


@JWT_MANAGER.unauthorized_loader
def missing_token_callback(error):
    raise exceptions.JWTError(
        "Missing JWT in cookies or headers: %s" % str(error), 401)


@JWT_MANAGER.needs_fresh_token_loader
def token_not_fresh_callback():
    raise exceptions.JWTError(
        "Fresh token required, this token is not fresh", 401)


@JWT_MANAGER.revoked_token_loader
def revoked_token_callback():
    raise exceptions.JWTError("The token sent is revoked", 401)
