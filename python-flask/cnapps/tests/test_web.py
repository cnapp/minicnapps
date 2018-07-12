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

from jinja2 import TemplateNotFound
import unittest
from unittest import mock

from cnapps import version
from cnapps import web


class WebTest(unittest.TestCase):
    """Test the Web module

    """

    content = ""

    def setUp(self):
        with open("ChangeLog.md", "r") as inputfile:
            self.content = inputfile.read()

    @mock.patch("flask.render_template")
    def test_home_page(self, mock_render):
        """Test the home page rendering function

        :param mock_render:
        :return:
        """
        rendered = "<aHtmlPage>"
        mock_render.return_value = rendered
        self.assertEqual(rendered, web.home_page())
        mock_render.assert_called_once_with(
            "home.html", version=version.RELEASE
        )

    @mock.patch("flask.render_template")
    def test_home_page_template_not_found(self, mock_render):
        """Test the home page rendering function (template not found)

        The mock is called twice:
        - the fist time, it raises an Exception
        - the 2nd time, it returns the template
        :param mock_render:
        :return:
        """
        err_message = "problem with template engine"
        rendered = "<aHtmlPage>"
        mock_render.side_effect = [TemplateNotFound(err_message), rendered]
        web.home_page()
        self.assertEqual(2, mock_render.call_count)

    @mock.patch("flask.render_template")
    def test_home_page_template_not_found_definitely(self, mock_render):
        """Test the home page rendering function (template not found)

        The mock is called twice:
        - the fist time, it raises an Exception
        - the 2nd time, it raises an Exception again, so an error is got
        :param mock_render:
        :return:
        """
        err_message = "problem with template engine"
        mock_render.side_effect = [
            TemplateNotFound(err_message),
            TemplateNotFound(err_message),
        ]
        self.assertEqual(web.home_page(), "Not Found. " + err_message)
        self.assertEqual(2, mock_render.call_count)

    @mock.patch("flask.render_template")
    def test_changelog_page(self, mock_render):
        """Test the 'changelog_page' function

        """
        rendered = "<aHtmlPage>"
        mock_render.return_value = rendered
        self.assertEqual(rendered, web.changelog_page())
        mock_render.assert_called_once_with(
            "changelog.html", content=self.content, version=version.RELEASE
        )
