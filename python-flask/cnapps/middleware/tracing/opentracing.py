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
from os import environ

import jaeger_client
from jaeger_client import config
from opentracing.ext import tags

from cnapps import settings


LOGGER = logging.getLogger(__name__)

TAG_USER = "user"


def get_commons_tags(component, method, status_code):
    return {
        tags.SPAN_KIND: tags.SPAN_KIND_RPC_SERVER,
        tags.COMPONENT: component,
        tags.HTTP_STATUS_CODE: status_code,
        tags.HTTP_METHOD: method,
    }


def set_common_tags(span, component, method, user=None):
    span.set_tag(tags.SPAN_KIND, tags.SPAN_KIND_RPC_SERVER)
    span.set_tag(tags.COMPONENT, component)
    # span.set_tag(tags.HTTP_STATUS_CODE, status_code)
    span.set_tag(tags.HTTP_METHOD, method)
    if user:
        span.set_tag(TAG_USER, user)


def set_tag_response_code(span, status_code):
    span.set_tag(tags.HTTP_STATUS_CODE, status_code)


def init_tracer(service):
    """Initialize an OpenTracing tracer.

    Args:
        service ([string]): the name of the service

    Returns:
        [tracer]: an OpenTracing tracer
    """

    agent = environ.get("TRACING_AGENT_ADDR", settings.DEFAULT_TRACING_ADDR)
    LOGGER.info("Initialize Jaeger client for service: %s %s", service, agent)
    tracer_conf = jaeger_client.Config(
        config={
            "sampler": {"type": "const", "param": 1},
            "local_agent": {
                "reporting_host": agent,
                "reporting_port": config.DEFAULT_REPORTING_PORT,
            },
            "logging": True,
            "reporter_batch_size": 1,
        },
        service_name=service,
    )

    # this call also sets opentracing.tracer
    return tracer_conf.initialize_tracer()
