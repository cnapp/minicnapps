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

import json
import logging
import secrets
import unittest
from unittest import mock

from cnapps import application
from cnapps.middleware.auth import jwt as jwt_auth
from cnapps.middleware.auth import request
from cnapps.middleware.logging import log
from cnapps.tests import settings

LOGGER = logging.getLogger(__name__)

ALPHABET = "abcdefghijklmnopqrstuvwxyz0123456789"


log.setup_logging()


class CnappsTestCase(unittest.TestCase):

    # def setUp(self):
        # commons.db.create_all()

    # def tearDown(self):
        # commons.db.session.remove()
        # commons.db.drop_all()

    def check_content_type(self, response):
        LOGGER.info("Response: %s %s", response.status, response.data)
        self.assertEqual(
            "application/json", response.headers.get("Content-Type")
        )

    def check_rest_error(self, response, http_status, err_type):
        LOGGER.info("Response: %s %s", response.status, response.data)
        self.assertEqual(http_status, response.status)
        if response.status != "204 NO CONTENT":
            err = json.loads(response.data.decode("utf8"))
            self.assertFalse(err["success"])
            self.assertEqual(err_type, err["error"]["type"])


class CnappsUnitTestCase(CnappsTestCase):
    """Base class to inherit test cases."""

    @classmethod
    @mock.patch("cnapps.application.setup_tracing")
    @mock.patch("cnapps.application.setup_configuration")
    @mock.patch("cnapps.application.setup_authentication")
    def setUpClass(
        cls, mock_setup_auth, mock_setup_conf, mock_setup_tracing
    ):
        mock_setup_conf.return_value = True
        mock_setup_auth.return_value = True
        mock_setup_tracing.return_value = True

        if settings.DEBUG is True:
            logging.getLogger("sqlalchemy.engine").setLevel(logging.DEBUG)
        cls.app = application.creates_app()
        cls.app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
        cls.app.tracer = mock.MagicMock()
        jwt_auth.setup(cls.app)
        cls.app_client = cls.app.test_client()
        cls.app_context = cls.app.test_request_context()
        cls.app_context.push()



def random_string(strlen):
    result = ""
    for i in range(strlen):
        result += secrets.choice(ALPHABET)
    return result


def random_number(below=1000):
    return secrets.randbelow(below)
