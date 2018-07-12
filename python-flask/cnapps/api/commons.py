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

from cnapps.middleware.tracing import opentracing


LOGGER = logging.getLogger(__name__)


def make_webservice_response(data, status_code=200, message=None):
    """Creates the HTTP response.

    Args:
        data ([json]): The JSON content to send.
        status_code ([int], optional): Defaults to 200. The HTTP status code.
        message ([string], optional): Defaults to None. The response message

    Returns:
        A HTTP response.
    """

    response = flask.jsonify({"status": status_code, "message": message})
    response.status_code = status_code
    response.data = data
    response.headers["Content-Type"] = "application/json"
    LOGGER.info("Response: %s %s", status_code, data)
    LOGGER.info("Response: %s", response)
    return response


def make_response(message, code, parent_span=None):
    """Creates a HTTP response in JSON (application/json content-type)

    Args:
        message ([string]): The response message
        code ([int]): The HTTP status code.
        parent_span ([opentracing.span], optional): An OpenTracing span to add
            a trace

    Returns:
        A HTTP response.
    """

    if parent_span:
        opentracing.set_tag_response_code(parent_span, code)
        with flask.current_app.tracer.start_span(
            "response", child_of=parent_span
        ) as span:
            span.log_kv({"response": message.json})
    resp = message
    resp.status_code = code
    return resp
