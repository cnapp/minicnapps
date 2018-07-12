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
from unittest import mock

from cnapps.middleware.metrics import prometheus


class PrometheusTest(unittest.TestCase):
    """Test the 'prometheus' module

    """

    @mock.patch("prometheus_client.core._LabelWrapper.labels", autospec=True)
    def test_set_status_metrics_ko(self, mock_gauge):
        services = []
        statuses = {
            "global_status": "ko",
        }
        prometheus.set_status_metrics(statuses, services)
        self.assertEqual(1, mock_gauge.call_count)

    @mock.patch("prometheus_client.core._LabelWrapper.labels", autospec=True)
    def test_set_status_metrics_ok(self, mock_gauge):
        services = []
        statuses = {
            "global_status": "ok",
        }
        prometheus.set_status_metrics(statuses, services)
        self.assertEqual(1, mock_gauge.call_count)

    @mock.patch("flask.make_response", autospec=True)
    @mock.patch("prometheus_client.core.REGISTRY", autospec=True)
    @mock.patch(
        "prometheus_client.exposition.CONTENT_TYPE_LATEST", autospec=True
    )
    @mock.patch("prometheus_client.exposition.generate_latest", autospec=True)
    # @mock.patch("cnapps.dao.commons.check_sql", autospec=True)
    @mock.patch("prometheus_client.core._LabelWrapper.labels", autospec=True)
    def test_show_metrics(
        self,
        mock_gauge,
        # mock_sql,
        mock_output,
        mock_content_type,
        mock_registry,
        mock_resp,
    ):
        mock_content_type.return_value = str(
            "text/plain; version=0.0.4; charset=utf-8"
        )
        self.assertIsNotNone(prometheus.show_metrics())
        self.assertEqual(1, mock_gauge.call_count)
        # self.assertEqual(1, mock_sql.call_count)
        self.assertEqual(1, mock_output.call_count)
        self.assertEqual(0, mock_registry.call_count)  # Not a callable
        self.assertEqual(1, mock_resp.call_count)
