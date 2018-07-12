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

from cnapps.api import commons
from cnapps import version


REST = flask.Blueprint("version", __name__)

LOGGER = logging.getLogger(__name__)


@REST.route("/version", methods=["GET"])
def version_status():
    """Display application version.

    Returns:
        A HTTP response in JSON (application/json content-type)
    """

    LOGGER.info("Get version")
    return commons.make_webservice_response(
        flask.json.dumps({"version": version.RELEASE})
    )
