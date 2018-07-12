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

from cnapps import exceptions
from cnapps import settings

LOGGER = logging.getLogger(__name__)


def load_configuration():
    """Load configuration from environment variables"""

    if settings.ENV_DB_ENGINE not in os.environ:
        LOGGER.error(
            "Can't retrieve database engine from environment. "
            "Set %s" % settings.ENV_DB_ENGINE)
        raise exceptions.ConfigurationError("Database engine not set")
    return {
        "database": os.environ[settings.ENV_DB_ENGINE]
    }
