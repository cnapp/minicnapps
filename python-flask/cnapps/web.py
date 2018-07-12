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
from os import path

import flask
import jinja2

from cnapps import version


REST = flask.Blueprint("web", __name__, template_folder="templates")

LOGGER = logging.getLogger(__name__)


def render_page(page, **context):
    """Render a HTML page.

    :param page: the template name
    """

    try:
        LOGGER.info("Render web page: %s", page)
        return flask.render_template(page, version=version.RELEASE)

    except jinja2.TemplateNotFound as err:
        msg = "Can't load template: %s" % str(err)
        LOGGER.warn(msg)
        try:
            return flask.render_template(
                "error.html", error_message=msg, version=version.RELEASE
            )

        except jinja2.TemplateNotFound as err:
            LOGGER.error("Can't find error template")
            return "Not Found. %s" % err.message


def read_file_content(filename):
    with open(filename, "r") as inputfile:
        return inputfile.read()


@REST.route("/")
def home_page():
    return render_page("home.html")


@REST.route("/changelog")
def changelog_page():
    content = None
    if path.exists("ChangeLog.md"):
        content = read_file_content("ChangeLog.md")
    elif path.exists("/srv/ChangeLog.md"):
        content = read_file_content("/srv/ChangeLog.md")

    return flask.render_template(
        "changelog.html", content=content, version=version.RELEASE
    )


@REST.route("/favicon.ico")
def favicon():
    return flask.redirect(
        flask.url_for("static", filename="img/favicon.ico"), code=302
    )
