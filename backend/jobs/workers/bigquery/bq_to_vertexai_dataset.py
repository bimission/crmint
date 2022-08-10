# Copyright 2021 Google Inc. All rights reserved.
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

import google.auth
from google.cloud import aiplatform
from jobs.workers.vertexai.vertexai_worker import VertexAIWorker


class BQToVertexAIDataset(VertexAIWorker):
  """Worker to export a BigQuery table to a Vertex AI dataset."""

  PARAMS = [
      ('bq_project_id', 'string', True, '', 'BQ Project ID'),
      ('bq_dataset_id', 'string', True, '', 'BQ Dataset ID'),
      ('bq_table_id', 'string', True, '', 'BQ Table ID'),
      ('bq_dataset_location', 'string', True, '', 'BQ Dataset Location'),
      ('vertexai_region', 'string', True, '', 'Vertex AI Region'),
      ('vertexai_dataset_name', 'string', False, '', 'Vertex AI Dataset Name'),
      ('clean_up', 'boolean', True, True, 'Clean Up'),
  ]

  def _execute(self):
    aiplatform.init(
        project=self._get_project_id(),
        location=self._params['vertexai_region'],
    )
    project_id = self._params['bq_project_id']
    dataset_id = self._params['bq_dataset_id']
    table_id = self._params['bq_table_id']
    vertexai_region = self._params['vertexai_region']
    vertexai_dataset_name = self._params['vertexai_dataset_name']
    dataset_client = self._get_vertexai_dataset_client(vertexai_region)
    if not vertexai_dataset_name:
      display_name = f'{project_id}.{dataset_id}.{table_id}'
    else:
      display_name = vertexai_dataset_name
    if self._params['clean_up']:
      try:
        datasets = dataset_client.list_datasets({
            'parent': self._get_parent_resource(vertexai_region),
            'filter': f'display_name="{display_name}"',
            'order_by': 'create_time asc'})
        if datasets:
          for d in list(datasets)[:-1]:
            dataset_client.delete_dataset({'name': d.name})
            self.log_info(f'Deleted dataset: {d.name}')
      except Exception as e:
        self.log_info(f'Exception: {e}')
    dataset = aiplatform.TabularDataset.create(
        display_name=display_name,
        bq_source=f'bq://{project_id}.{dataset_id}.{table_id}')
    dataset.wait()
    self.log_info(f'Dataset created: {dataset.resource_name}')
    self.log_info('Finished successfully')
