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

from cnapps.api.v1 import core


API_DOC_AUTH = "%s.auth" % core.PATH

API_DOC_CONTACTS = "%s.contacts" % core.PATH

API_DOC_CUSTOMERS = "%s.customers" % core.PATH

API_DOC_ENVIRONMENTS = "%s.environments" % core.PATH

API_DOC_ENVIRONMENT_TYPES = "%s.environment_types" % core.PATH

API_DOC_PROJECTS = "%s.projects" % core.PATH

API_DOC_VMS = "%s.virtualmachines" % core.PATH

API_DOC_PROVIDERS = "%s.providers" % core.PATH

API_DOC_PROVIDER_TYPES = "%s.provider_types" % core.PATH

API_DOC_IP_ADDRESS = "%s.ip_addresses" % core.PATH

API_DOC_API_KEY = {
    "description": "Custom HTTP header which contains the token",
    "in": "header",
    "type": "string",
    "required": False,
}

API_DOC_USERID = {
    "description": "Custom HTTP header which contains the UserID",
    "in": "header",
    "type": "string",
    "required": False,
}

API_DOC_USER_KEY = {
    "description": "Custom HTTP header which contains the username account",
    "in": "header",
    "type": "string",
    "required": True,
}

API_DOC_PASSWORD_KEY = {
    "description": "Custom HTTP header which contains the password account",
    "in": "header",
    "type": "string",
    "required": True,
}

API_DOC_TOKEN = {
    "description": "HTTP header which contains the JWT token : Bearer TOKEN",
    "in": "header",
    "type": "string",
    "required": False,
}
