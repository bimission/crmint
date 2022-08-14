import pytest
from unittest import mock
from importlib import reload
from unittest.mock import patch
from google import auth
from google.auth import credentials as auth_credentials

from absl.testing import absltest
from absl.testing import parameterized
from google.auth import credentials
from google.cloud import aiplatform
from google.cloud.aiplatform import datasets
from google.cloud.aiplatform import initializer
from google.cloud.aiplatform import schema
from google.cloud.aiplatform.compat.services import dataset_service_client
from google.cloud.aiplatform.compat.types import (
  dataset as gca_dataset,
  dataset_service as gca_dataset_service
)
from google.api_core import operation

from jobs.workers.bigquery import bq_to_vertexai_dataset

_TEST_PROJECT = "test-project"
_TEST_LOCATION = "us-central1"

# dataset
_TEST_ID = "1028944691210842416"
_TEST_DISPLAY_NAME = "my_dataset_1234"
_TEST_TABLE_NAME = "my_table_1234"
_TEST_DESCRIPTION = "test description"

# metadata_schema_uri
_TEST_METADATA_SCHEMA_URI_TABULAR = schema.dataset.metadata.tabular
_TEST_SOURCE_URI_BQ = "bq://my-project.my-dataset.table"
_TEST_RESOURCE_NAME = f"projects/{_TEST_PROJECT}/locations/{_TEST_LOCATION}/datasets/{_TEST_ID}"

_TEST_METADATA_TABULAR_BQ = {
  "inputConfig": {"bigquerySource": {"uri": _TEST_SOURCE_URI_BQ}}
}








def _make_credentials():
  creds = mock.create_autospec(
    credentials.Credentials, instance=True, spec_set=True)
  return creds



class BQToVertexAIDatasetExporterTest(parameterized.TestCase):


    @parameterized.parameters(
      {
        'cfg_vertexai_dataset_name': _TEST_DISPLAY_NAME,
        'cfg_clean_up': True
      },
      {
        'cfg_vertexai_dataset_name': _TEST_DISPLAY_NAME,
        'cfg_clean_up': False
      },
      {
        'cfg_vertexai_dataset_name': None,
        'cfg_clean_up': True
      },
    )
    def test_create_veretxai_dataset(self,
         cfg_vertexai_dataset_name, cfg_clean_up):
      worker_inst = bq_to_vertexai_dataset.BQToVertexAIDataset(
        ##params
        {
          'vertexai_dataset_name': cfg_vertexai_dataset_name,
          'clean_up': cfg_clean_up,
        },
        ##pipeline_id: int,
        pipeline_id=1,
        ##job_id: int,
        job_id=1,
        ##logger_project: Optional[str] = None,
        logger_project=_TEST_PROJECT,
        ##logger_credentials: Optional[credentials.Credentials] = None
        logger_credentials=_make_credentials()
      )


      if not cfg_vertexai_dataset_name:
        display_name = f'{_TEST_PROJECT}.{_TEST_DISPLAY_NAME}.{_TEST_TABLE_NAME}'
      else:
        display_name = cfg_vertexai_dataset_name


      mock_datasets_client = mock.create_autospec(
         dataset_service_client.DatasetServiceClient, instance=True, spec_set=True)


      mock_dataset = mock.Mock(gca_dataset.Dataset(
        display_name=display_name,
        metadata_schema_uri=_TEST_METADATA_SCHEMA_URI_TABULAR,
        metadata=_TEST_METADATA_TABULAR_BQ,
        name=display_name
      ))


      mock_datasets_client.list_datasets.return_value = [mock_dataset, mock_dataset]

      delete_dataset_lro_mock = mock.Mock(operation.Operation)
      delete_dataset_lro_mock.result.return_value = (
        gca_dataset_service.DeleteDatasetRequest()
      )

      mock_datasets_client.delete_dataset.return_value = delete_dataset_lro_mock

      mock_tabular_dataset = mock_dataset
      mock_tabular_dataset.resource_name = _TEST_RESOURCE_NAME

      mock_tabular_dataset.wait = mock.Mock(True)


      mocked_tablular_dataset_client = mock.create_autospec(
        aiplatform.datasets.tabular_dataset.TabularDataset, instance=True, spec_set=True)
      mocked_tablular_dataset_client.create.return_value = mock_tabular_dataset


      self.enter_context(
        mock.patch.object(
          worker_inst,
          '_get_project_id',
          return_value=_TEST_PROJECT,
          autospec=True,
          spec_set=True
        )
      )

      self.enter_context(
        mock.patch.object(
          worker_inst,
          '_get_vertexai_dataset_client',
          return_value=mock_datasets_client,
          autospec=True,
          spec_set=True
        )
      )

      self.enter_context(
        mock.patch.object(
          worker_inst,
          '_get_tabular_dataset_client',
          return_value=mocked_tablular_dataset_client,
          autospec=True,
          spec_set=True
        )
      )

      self.enter_context(
        mock.patch.object(
          worker_inst,
          'log_info',
          return_value="logger",
          autospec=True,
          spec_set=True
        )
      )

      worker_inst._execute()
      ## asserts
      if cfg_clean_up:
         mock_datasets_client.list_datasets.assert_called_once()
         mock_datasets_client.delete_dataset.assert_called_once()
      mocked_tablular_dataset_client.create.assert_called_once()


if __name__ == '__main__':
  absltest.main()
