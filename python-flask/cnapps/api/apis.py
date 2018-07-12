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
from cnapps.api import docs
from cnapps.api.v1 import core as v1_core
from cnapps.api.v1alpha import core as v1alpha_core


REST = flask.Blueprint("apis", __name__)

API_PATH = "/api/apis"

LOGGER = logging.getLogger(__name__)

MA = flask_marshmallow.Marshmallow()


class APIVersionSchema(MA.Schema):

    name = marshmallow.fields.Str()

    class Meta(object):
        strict = True


API_SCHEMA = APIVersionSchema()
API_SCHEMAS = APIVersionSchema(many=True)


@REST.route(API_PATH, methods=["GET"])
@flask_apispec.doc(
    description="Retrieve available API versions",
    responses={
        "200": {"description": "Success", "schema": API_SCHEMAS},
        "500": {"description": "If an unexpected error occurs"},
    },
    tags=[docs.API_DOC_APIS],
)
@flask_apispec.marshal_with(API_SCHEMAS)
def version_status():
    """Get available API versions

    Returns:
        A HTTP response in JSON (application/json content-type)
    """

    LOGGER.info("Get API versions")
    apis = []
    apis.append({"name": v1_core.PATH})
    apis.append({"name": v1alpha_core.PATH})
    return commons.make_webservice_response(flask.json.dumps(apis))
