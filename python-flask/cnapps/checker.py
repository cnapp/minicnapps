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

from sqlalchemy import exc

from cnapps.dao import commons as dao_commons


LOGGER = logging.getLogger(__name__)

STATUS_OK = "ok"
STATUS_KO = "ko"


def global_status():
    LOGGER.info("Check global status")
    status = {}
    status["global_status"] = STATUS_OK

    sql_check = database()
    status["database"] = sql_check
    if sql_check["database_status"] == STATUS_KO:
        status["global_status"] = STATUS_KO

    return status


def database():
    LOGGER.info("Check database")
    status = {}
    status["database_status"] = STATUS_OK
    try:
        sql = []
        result = dao_commons.check_sql()
        for data in result:
            sql.append("%s" % data)
        status["version"] = sql
        status["database_status"] = STATUS_OK

    except exc.SQLAlchemyError as err:
        LOGGER.error("Can't check database: %s", str(err))
        status["version"] = str(err)
        status["database_status"] = STATUS_KO
    return status
