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

from cnapps import exceptions


LOGGER = logging.getLogger(__name__)

REST = flask.Blueprint("errors", __name__)


def debug_error(error):
    message = [str(x) for x in error.args]
    if not message:
        message = error.message
    LOGGER.debug("Error: %s", message)


@REST.app_errorhandler(exceptions.CnappsError)
def handle_error(error):
    LOGGER.info("Handle error: %s %s", error.__class__.__name__, error)

    message = error.message
    status_code = error.status_code
    success = False
    response = {
        "success": success,
        "error": {
            "type": error.__class__.__name__,
            "message": message,
            "code": status_code,
        },
    }

    return flask.jsonify(response), status_code


@REST.app_errorhandler(Exception)
def handle_unexpected_error(error):
    LOGGER.error(
        "Handle unexpected error: %s %s", error.__class__.__name__, error
    )
    status_code = 500
    success = False
    description = [str(x) for x in error.args]
    if not description:
        description = error
    response = {
        "success": success,
        "error": {
            "type": "UnexpectedException",
            "message": "An unexpected error has occurred.",
            "description": description,
        },
    }

    return flask.jsonify(response), status_code
