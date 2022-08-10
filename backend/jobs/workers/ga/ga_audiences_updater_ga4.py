# Copyright 2022 Google Inc. All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Worker to update Google Analytics remarketing audiences."""

from google.analytics.admin import AnalyticsAdminServiceClient

from jobs.workers.bigquery import bq_worker

class GA4AudiencesUpdater(bq_worker.BQWorker):
  """Worker to update GA audiences using values from a BigQuery table.

  For more details on the required GA Audience JSON template format, see:
  https://developers.google.com/analytics/devguides/config/mgmt/v3/mgmtReference/management/remarketingAudience#resource.
  """

  PARAMS = [
      ('property_id', 'string', True, '',
       'GA Property Tracking ID (e.g. 12345)'),
  ]

  def _execute(self) -> None:
    ga_client = AnalyticsAdminServiceClient()
    property_id = self._params['property_id']
    audiences = ga_client.list_audiences(
        parent=f"properties/{property_id}")
    for audience in audiences:
      self.log_info(f'{audience}')
