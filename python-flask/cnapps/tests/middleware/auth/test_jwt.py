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

import jwt

from cnapps.middleware.auth import jwt as jwt_auth
from cnapps.tests import commons


class FixtureKeystoneRole(object):
    def __init__(self, role_id, name):
        self.id = role_id
        self.name = name


class FixtureKeystoneUser(object):
    def __init__(self, user_id, name):
        self.id = user_id
        self.name = name

    def __repr__(self):
        return "<FixtureKeystoneUser(%s, %s)" % (self.id, self.name)


class JWTAuthTestCase(commons.CnappsUnitTestCase):

    def test_create_tokens(self):
        user = FixtureKeystoneUser(commons.random_string(10), "user1")
        roles = [
            FixtureKeystoneRole(commons.random_string(10), "role1"),
            FixtureKeystoneRole(commons.random_string(10), "role2"),
        ]
        result = jwt_auth.create_tokens(user, roles)
        print("Tokens: %s", result)
        self.assertIsNotNone(result['access_token'])
        decoded_token = jwt.decode(
            result['access_token'], 'my-secret', algorithms=['HS256'])
        self.assertEqual(user.id, decoded_token['identity']['userid'])
        self.assertEqual(
            ["role1", "role2"], decoded_token['identity']['roles'])
