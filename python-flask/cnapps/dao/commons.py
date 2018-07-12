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

import datetime
import logging

import flask_marshmallow
import flask_sqlalchemy
from sqlalchemy import exc

from cnapps import exceptions
from cnapps.utils import errors


db = flask_sqlalchemy.SQLAlchemy()
ma = flask_marshmallow.Marshmallow()

LOGGER = logging.getLogger(__name__)

CREATE_ERR = "An error occurs during SQL request to " "create the entity."

UPDATE_ERR = "An error occurs during SQL request to " "update the entity."

DELETE_ERR = "An error occurs during SQL request to " "delete the entity."


def check_sql():
    """Check SQL connection.

    Raises:
        exceptions.DatabaseError: if an error occurs during SQL execution

    Returns:
        version: which version of SQL server is
    """

    try:
        LOGGER.info("Check SQL version: %s", db.engine.name)
        if db.engine.name == "sqlite":
            return db.engine.execute("select sqlite_version()")
        return db.engine.execute("SELECT version() AS value")

    except exc.SQLAlchemyError as err:
        errors.stracktrace()
        raise exceptions.DatabaseError("Can't check SQL version") from err


def entity_id(prefix):
    """Creates a new ID for an entity

    Args:
        prefix ([string]): a prefix to add to the ID

    Returns:
        A string which represents the entity ID
    """

    current_date = datetime.datetime.now()
    return "%sID%s" % (prefix, current_date.strftime("%Y%m%d%H%M%S%f"))


def list_entities(model, err_msg):
    """List some SQL entities.

    Args:
        model ([db.Model]): the database model to use
        err_msg ([string]): the error message if an error occurs

    Raises:
        exceptions.DatabaseError: if an error occurs during SQL execution

    Returns:
        A list of database models
    """

    LOGGER.debug("List entities %s", model)
    try:
        return model.query.order_by(model.id).all()

    except exc.SQLAlchemyError as err:
        errors.stracktrace()
        raise exceptions.DatabaseError(err_msg) from err


def get_entity(model, id, err_msg):
    """Retrieve a SQL entity.

    Args:
        model ([db.Model]): the database model to use
        id ([int]): the entity ID
        err_msg ([string]): the error message if an error occurs

    Raises:
        exceptions.DatabaseError: if an error occurs during SQL execution

    Returns:
        A database model entity
    """

    LOGGER.debug("Get entity %s id=%s", model, id)
    try:
        return model.query.filter_by(id=id).first()

    except exc.SQLAlchemyError as err:
        errors.stracktrace()
        raise exceptions.DatabaseError(err_msg) from err


def add_entity(entity):
    """Add into database an entity.

    Args:
        entity ([db.Model]): the object to add into the database

    Raises:
        exceptions.DatabaseError: if an error occurs during SQL execution

    Returns:
        A database model entity
    """

    LOGGER.debug("Add entity %s", entity)
    try:
        entity.created_at = datetime.datetime.now()
        db.session.add(entity)
        db.session.commit()
        return entity

    except exc.SQLAlchemyError as err:
        errors.stracktrace()
        db.session.rollback()
        raise exceptions.DatabaseError(CREATE_ERR) from err


def delete_entity(entity, soft=True):
    """Remove an object from the database.

    :param entity: the object to remove
    """

    LOGGER.debug("Delete entity %s", entity)
    try:
        entity.deleted_at = datetime.datetime.now()
        if soft is None:
            db.session.delete(entity)
        db.session.commit()
        return entity

    except exc.SQLAlchemyError as err:
        errors.stracktrace()
        db.session.rollback()
        raise exceptions.DatabaseError(DELETE_ERR) from err


def update_entity(entity):
    """Update values of an object into the database.

    :param entity: the object to update values.
    """

    LOGGER.debug("Update entity %s", entity)
    try:
        entity.updated_at = datetime.datetime.now()
        db.session.commit()
        return entity

    except exc.SQLAlchemyError as err:
        errors.stracktrace()
        db.session.rollback()
        raise exceptions.DatabaseError(UPDATE_ERR) from err
