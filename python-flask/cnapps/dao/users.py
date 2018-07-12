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

import marshmallow
from sqlalchemy import exc

from cnapps.dao import commons
from cnapps import exceptions
from cnapps.utils import errors


LOGGER = logging.getLogger(__name__)

ALL_USERS_ERR = (
    "An error occurs during SQL request to " "retrieve all Users."
)

GET_USER_ERR = (
    "An error occurs during SQL request to " "retrieve the User."
)

CREATE_USER_ERR = (
    "An error occurs during SQL request to " "create the User."
)


class User(commons.db.Model):
    __tablename__ = "user"

    id = commons.db.Column("user_id", commons.db.Integer, primary_key=True)
    name = commons.db.Column("name", commons.db.String(50))
    email = commons.db.Column("email", commons.db.String(150))
    created_at = commons.db.Column("created_at", commons.db.DateTime)
    updated_at = commons.db.Column("updated_at", commons.db.DateTime)
    deleted_at = commons.db.Column("deleted_at", commons.db.DateTime)

    def __init__(self, name, email):
        self.name = name
        self.email = email

    def __repr__(self):
        return (
            "<User(id=%s, name=%s, email=%s "
            "createdAt=%s, updatedAt=%s, deletedAt=%s)>"
            % (
                self.id,
                self.name,
                self.email,
                self.created_at,
                self.updated_at,
                self.deleted_at,
            )
        )


class UserSchema(commons.ma.Schema):

    id = marshmallow.fields.Integer()
    name = marshmallow.fields.Str()
    email = marshmallow.fields.Str()
    createdAt = marshmallow.fields.DateTime(
        attribute="created_at", dump_only=True)
    updatedAt = marshmallow.fields.DateTime(
        attribute="updated_at", dump_only=True)
    deletedAt = marshmallow.fields.DateTime(
        attribute="deleted_at", dump_only=True)

    class Meta(object):
        strict = True


USER_SCHEMA = UserSchema()
USERS_SCHEMA = UserSchema(many=True)



def get_all():
    """Retrieve all users.

    Raises:
        exceptions.DatabaseError: if an errors occurs during SQL execution

    Returns:
        [list]: A list of User model
    """

    LOGGER.info("Search all users")
    return commons.list_entities(User, ALL_USERS_ERR)


def get_User(id):
    """Retrieve a user.

    Args:
        id ([int]): the ID of the User model.

    Raises:
        exceptions.DatabaseError: if an errors occurs during SQL execution

    Returns:
        [User]: A User model
    """

    LOGGER.info("Get a user with ID %s", id)
    return commons.get_entity(User, id, GET_USER_ERR)


def get_user_by_name(name):
    """Retrieve a user.

    Args:
        name ([string]): the name of the user to retrieve

    Raises:
        exceptions.DatabaseError: if an errors occurs during SQL execution

    Returns:
        [User]: A User model
    """

    LOGGER.info("Get a User with name %s", name)
    try:
        return User.query.filter_by(name=name).first()

    except exc.SQLAlchemyError as err:
        errors.stracktrace()
        raise exceptions.DatabaseError(GET_USER_ERR) from err


def create_User(name, email):
    """Create a new User.

    Args:
        name ([string]): The name of the User
        email ([string]): An email

    Raises:
        exceptions.DatabaseError: if an errors occurs during SQL execution

    Returns:
        [User]: A User model
    """

    LOGGER.info("Create a User %s %s", name, email)
    try:
        return commons.add_entity(User(name, email))

    except exc.SQLAlchemyError as err:
        errors.stracktrace()
        raise exceptions.DatabaseError(CREATE_USER_ERR) from err
