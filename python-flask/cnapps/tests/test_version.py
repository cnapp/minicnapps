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

import unittest

from cnapps import version


class VersionTest(unittest.TestCase):
    """Test the correct format of version

    """

    def test_check_version(self):
        """Checks 'release' variable is correctly set in 'version.py' file.

        """
        self.assertRegexpMatches(
            version.RELEASE, "^([0-9]+)([.])([0-9]+)([.])([0-9]+)[\-a-z0-9]*$"
        )
