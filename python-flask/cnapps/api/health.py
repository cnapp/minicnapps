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
from cnapps import checker
from cnapps.middleware.auth import request
from cnapps.middleware.metrics import prometheus
from cnapps.middleware.tracing import opentracing


REST = flask.Blueprint("health", __name__)

LOGGER = logging.getLogger(__name__)

API_PATH = "/health"


@REST.route("%s" % API_PATH, methods=["GET"])
def api_health_status():
    """Check application healthz.

    Returns:
        A HTTP response in JSON (application/json content-type)
    """

    LOGGER.info("Check health")

    with flask.current_app.tracer.start_span("health") as parent_span:
        opentracing.set_common_tags(parent_span, "health", "GET")

        with flask.current_app.tracer.start_span(
            "check", child_of=parent_span
        ) as span:
            status = checker.global_status()
            span.log_kv({"status": status})
            prometheus.API_USER.labels(API_PATH, 200, "None").inc()
            return commons.make_response(
                flask.jsonify(status), 200, parent_span
            )
