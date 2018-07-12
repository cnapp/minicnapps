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

from io import StringIO
import sys
import unittest
from unittest import mock

from cnapps import errors
from cnapps.utils import errors as utils_errors


class FixtureError(object):
    def __init__(self, message, status_code):
        self.message = message
        self.status_code = status_code
        self.args = []


class ErrorsTest(unittest.TestCase):
    """Test the error management module

    """

    def test_debug_error(self):
        occurred_error = FixtureError("A new error has occurred", 0)
        captured_output = StringIO()
        sys.stderr = captured_output
        errors.debug_error(occurred_error)
        self.assertEqual("", captured_output.getvalue())

    @mock.patch("flask.jsonify", autospec=True)
    def test_handle_error(self, mock_jsonify):
        occurred_error = FixtureError("A new error has occurred", 400)
        resp, status = errors.handle_error(occurred_error)
        self.assertIsNotNone(resp)
        self.assertEqual(status, 400)
        self.assertEqual(1, mock_jsonify.call_count)

    @mock.patch("flask.jsonify", autospec=True)
    def test_handle_unexpected_error(self, mock_jsonify):
        occurred_error = FixtureError("A new error has occurred", 400)
        resp, status = errors.handle_unexpected_error(occurred_error)
        self.assertIsNotNone(resp)
        self.assertEqual(status, 500)
        self.assertEqual(1, mock_jsonify.call_count)

    def test_stacktrace(self):
        captured_output = StringIO()
        sys.stderr = captured_output
        bad_statement = None
        try:
            bad_statement = 10 / 0
        except ZeroDivisionError:
            utils_errors.stracktrace()
            self.assertIn("division by zero", captured_output.getvalue())
        self.assertIsNone(bad_statement)
