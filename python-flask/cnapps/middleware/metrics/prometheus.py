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
import time

import flask
import prometheus_client
from prometheus_client import core
from prometheus_client import exposition

from cnapps import checker


LOGGER = logging.getLogger(__name__)

REST = flask.Blueprint("prometheus", __name__)

GLOBAL_STATUS = prometheus_client.Gauge(
    "cnapps_pythonflask_up", "Was the last query of cnapps successful", ["service"]
)

REQUEST_LATENCY = prometheus_client.Histogram(
    "cnapps_pythonflask_request_latency_seconds",
    "Request Latency",
    ["method", "endpoint"],
)

REQUEST_COUNT = prometheus_client.Gauge(
    "cnapps_pythonflask_request_count",
    "Request Count",
    ["method", "endpoint", "status_code"],
)

API_USER = prometheus_client.Counter(
    "cnapps_pythonflask_api_usage",
    "API usage (count)",
    ["endpoint", "status_code", "user"],
)


def before_request():
    """Perform before each HTTP request."""

    flask.request.start_time = time.time()


def after_request(response):
    """Perform after each HTTP request."""

    request_latency = time.time() - flask.request.start_time
    REQUEST_LATENCY.labels(flask.request.method, flask.request.path).observe(
        request_latency
    )
    REQUEST_COUNT.labels(
        flask.request.method, flask.request.path, response.status_code
    ).inc()
    return response


def set_status_metrics(status, services):
    LOGGER.info("Application status: %s %s", status, services)
    GLOBAL_STATUS.labels("cnapps").set(1)
    for name in services:
        if status[name]["%s_status" % name] == "ko":
            GLOBAL_STATUS.labels(name).set(0)
            GLOBAL_STATUS.labels("cnapps").set(0)
        else:
            GLOBAL_STATUS.labels(name).set(1)


@REST.route("/metrics")
def show_metrics():
    """Display metrics for Prometheus."""
    status = checker.global_status()
    set_status_metrics(status, [])
    registry = core.REGISTRY
    output = exposition.generate_latest(registry)
    resp = flask.make_response(output, 200)
    resp.headers["Content-type"] = exposition.CONTENT_TYPE_LATEST
    return resp
