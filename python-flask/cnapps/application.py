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
import os
import types

import apispec
import flask
import flask_apispec

from cnapps.api import apis
from cnapps.api import health
from cnapps.api.v1 import auth
from cnapps.api.v1 import core as v1_core
from cnapps.api.v1alpha import core as v1alpha_core
from cnapps.api import version as api_version
from cnapps.dao import commons as dao_commons
from cnapps import errors
from cnapps import exceptions
from cnapps.middleware.config import environment
from cnapps.middleware.auth import jwt as jwt_auth
from cnapps.middleware.metrics import prometheus
from cnapps.middleware.tracing import opentracing
from cnapps import settings
from cnapps import version
from cnapps import web


LOGGER = logging.getLogger(__name__)


def creates_app():
    """Create the application

    Returns:
        [flask.Flask]: the main application
    """

    LOGGER.info("Create application %s", version.RELEASE)
    app = flask.Flask(
        __name__, static_folder="static", template_folder="templates"
    )
    # app.config.from_pyfile('settings.py')

    setup_configuration(app)
    setup_authentication(app)

    # Database
    dao_commons.db.init_app(app)
    dao_commons.ma.init_app(app)

    # API v1
    app.register_blueprint(apis.REST)
    app.register_blueprint(api_version.REST)
    app.register_blueprint(auth.REST)
    # API v1alpha

    app.register_blueprint(web.REST)

    setup_metrics(app)
    setup_tracing(app)
    app.register_blueprint(health.REST)
    app.register_blueprint(errors.REST)

    setup_apispec(app)
    return app


def setup_configuration(app):
    """Load configuration.

    Args:
        app ([flask.Flask]): the application

    Raises:
        exceptions.SecretError: if database password is not set
    """

    conf = environment.load_configuration()
    setup_database_configuration(app, conf)


def setup_database_configuration(app, conf):
    """Create database configuration

    Args:
        app ([flask.Flask]): the application
        conf ([dict]): the configuration loaded

    Raises:
        exceptions.SecretError: if key is not in environment variables
    """

    app.config["SQLALCHEMY_DATABASE_URI"] = conf["database"]
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    LOGGER.debug(
        "SQL configuration: %s", app.config["SQLALCHEMY_DATABASE_URI"]
    )


# def setup_auth_configuration(app, conf):
#     """Create authentication configuration

#     Args:
#         app ([flask.Flask]): the application
#         conf ([dict]): the configuration loaded

#     Raises:
#         exceptions.SecretError: [description]
#     """

#     if "KUBERNETES_SERVICE_HOST" in os.environ and (
#         os.environ.get("KUBE_NAME", "minikube") == "cloud"
#     ):
#         LOGGER.info("In Kubernetes use Vault for secure data")
#         vault_client = vault.create_client(conf)
#         vault_client.setup()
#         secrets = vault_client.read("compte_service_adsubs")
#         user_password = secrets["password"]
#     else:
#         if settings.cnapps_USER_SERVICE_PASSWORD not in os.environ:
#             LOGGER.error("Can't retrieve user password from environment")
#             raise exceptions.SecretError("Service user password not set")
#         user_password = os.environ[settings.cnapps_USER_SERVICE_PASSWORD]

#     app.config["auth"] = {
#         "auth_url": conf["identity"]["auth_url"],
#         "username": conf["identity"]["username"],
#         "user_domain_name": conf["identity"]["user_domain_name"],
#         "password": user_password,
#         "project_name": conf["identity"]["project_name"],
#         "project_domain_name": conf["identity"]["project_domain_name"],
#     }


def setup_metrics(app):
    """Setup metrics for Prometheus.

    Args:
        app ([flask.Flask]): the main application
    """

    LOGGER.debug("Setup Prometheus metrics")
    app.before_request(prometheus.before_request)
    app.after_request(prometheus.after_request)
    app.register_blueprint(prometheus.REST)


def setup_tracing(app):
    """Setup OpenTracing

    Args:
        app ([flask.Flask]): the main application
    """

    LOGGER.debug("Setup traces")
    tracer = opentracing.init_tracer(settings.APPNAME)
    if tracer:
        app.tracer = tracer


def setup_authentication(app):
    """Setup authentication.

    Args:
        app ([flask.Flask]): the application
    """

    jwt_auth.setup(app)


def setup_apispec(app):
    """Setup Swagger UI.

    Args:
        app ([flask.Flask]): the application
    """

    app.config.update(
        {
            "APISPEC_SPEC": apispec.APISpec(
                title="cnapps API",
                version="",
                info=dict(description="REST API of Cnapps."),
                plugins=("apispec.ext.marshmallow",),
            ),
            # 'APISPEC_SWAGGER_UI_URL': "/%s/swagger-ui" % core.PATH,
            # 'APISPEC_SWAGGER_URL': "/%s/swagger" % core.PATH,
        }
    )
    docs = flask_apispec.FlaskApiSpec(app)
    # PB: on a aussi l'API en defaults avec :
    # docs.register_existing_resources()
    v1_api_path = "/api/%s" % v1_core.PATH
    v1alpha_api_path = "/api/%s" % v1alpha_core.PATH
    for name, rule in app.view_functions.items():
        try:
            blueprint_name, _ = name.split(".")
            if isinstance(rule, types.FunctionType):
                paths = docs.view_converter.convert(rule, None, blueprint_name)
                LOGGER.debug("Endpoint: %s", paths[0]["path"])
                if paths[0]["path"].startswith(
                    v1_api_path) or paths[0]["path"].startswith(
                        v1alpha_api_path):
                    LOGGER.info("Add to Swagger: %s", paths[0]["path"])
                    docs.register(rule, blueprint=blueprint_name)
                elif paths[0]["path"].startswith("/api/apis"):
                    docs.register(rule, blueprint=blueprint_name)

        except ValueError:
            pass

        except TypeError:
            pass
