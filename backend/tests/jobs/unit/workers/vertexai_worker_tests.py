"""Tests for ga_waiter."""

from unittest import mock
from unittest.mock import patch
from absl.testing import absltest
from absl.testing import parameterized
from google.auth import credentials
from jobs.workers.vertexai import vertexai_worker
from google.cloud import aiplatform
from google.cloud.aiplatform.compat.services import pipeline_service_client
from google.cloud.aiplatform.compat.services import job_service_client
from google.cloud.aiplatform.compat.services import dataset_service_client
from google.cloud.aiplatform.compat.services import model_service_client
from google.cloud.aiplatform.compat.types import (
  pipeline_state as gca_pipeline_state,
  training_pipeline as gca_training_pipeline,
  batch_prediction_job as gca_batch_prediction_job,
  job_state as gca_job_state,
)
from jobs.workers.worker import WorkerException

_TEST_PROJECT = "test-project"
_TEST_LOCATION = "us-central1"

_TEST_DATASET_DISPLAY_NAME = "my_dataset_1234"
_TEST_DATASET_TABLE_NAME = "my_table_1234"

_TEST_VERETXAI_PREDICTION_JOB_NAME = "test-batch-prediction-job-name"
_TEST_VERETXAI_PREDICTION_JOB_ID = "abcdef123456"

_TEST_PIPELINE_RESOURCE_NAME = (
  "projects/my-project/locations/us-central1/trainingPipelines/12345"
)
_TEST_PIPELINE_NAME = "pipeline1234"

_TEST_BATCH_PREDICTION_JOB_NAME = "batchjob-123456"

def _make_credentials():
  return mock.create_autospec(
    credentials.Credentials, instance=True, spec_set=True)


class VertexAIWorkerTests(parameterized.TestCase):

  def test_get_vertexai_job_client(self):
    worker_inst = vertexai_worker.VertexAIWorker(
      ##params
      {},
      ##pipeline_id: int,
      pipeline_id=1,
      ##job_id: int,
      job_id=1,
      ##logger_project: Optional[str] = None,
      logger_project=_TEST_PROJECT,
      ##logger_credentials: Optional[credentials.Credentials] = None
      logger_credentials=_make_credentials()
    )

    mock_job_client = mock.create_autospec(
      job_service_client.JobServiceClient, instance=True, spec_set=True)

    with patch.object(worker_inst, '_get_vertexai_job_client', return_value = mock_job_client) as mock_vertexaicall:
       output = worker_inst._get_vertexai_job_client(_TEST_LOCATION)
       mock_vertexaicall.assert_called_once_with(_TEST_LOCATION)
       self.assertTrue(isinstance(output, job_service_client.JobServiceClient))

  def test_get_vertexai_pipeline_client(self):
    worker_inst = vertexai_worker.VertexAIWorker(
      ##params
      {},
      ##pipeline_id: int,
      pipeline_id=1,
      ##job_id: int,
      job_id=1,
      ##logger_project: Optional[str] = None,
      logger_project=_TEST_PROJECT,
      ##logger_credentials: Optional[credentials.Credentials] = None
      logger_credentials=_make_credentials()
    )

    mock_pipeline_client = mock.create_autospec(
      pipeline_service_client.PipelineServiceClient, instance=True, spec_set=True)

    with patch.object(worker_inst, '_get_vertexai_pipeline_client', return_value = mock_pipeline_client) as mock_vertexaicall:
      output = worker_inst._get_vertexai_pipeline_client(_TEST_LOCATION)
      mock_vertexaicall.assert_called_once_with(_TEST_LOCATION)
      self.assertTrue(isinstance(output, pipeline_service_client.PipelineServiceClient))

  def test_get_vertexai_dataset_client(self):
    worker_inst = vertexai_worker.VertexAIWorker(
      ##params
      {},
      ##pipeline_id: int,
      pipeline_id=1,
      ##job_id: int,
      job_id=1,
      ##logger_project: Optional[str] = None,
      logger_project=_TEST_PROJECT,
      ##logger_credentials: Optional[credentials.Credentials] = None
      logger_credentials=_make_credentials()
    )

    mock_dataset_client = mock.create_autospec(
      dataset_service_client.DatasetServiceClient, instance=True, spec_set=True)

    with patch.object(worker_inst, '_get_vertexai_dataset_client', return_value = mock_dataset_client) as mock_vertexaicall:
      output = worker_inst._get_vertexai_dataset_client(_TEST_LOCATION)
      mock_vertexaicall.assert_called_once_with(_TEST_LOCATION)
      self.assertTrue(isinstance(output, dataset_service_client.DatasetServiceClient))

  def test_get_vertexai_model_client(self):
    worker_inst = vertexai_worker.VertexAIWorker(
      ##params
      {},
      ##pipeline_id: int,
      pipeline_id=1,
      ##job_id: int,
      job_id=1,
      ##logger_project: Optional[str] = None,
      logger_project=_TEST_PROJECT,
      ##logger_credentials: Optional[credentials.Credentials] = None
      logger_credentials=_make_credentials()
    )

    mock_model_client = mock.create_autospec(
      model_service_client.ModelServiceClient, instance=True, spec_set=True)

    with patch.object(worker_inst, '_get_vertexai_model_client', return_value = mock_model_client) as mock_vertexaicall:
      output = worker_inst._get_vertexai_model_client(_TEST_LOCATION)
      mock_vertexaicall.assert_called_once_with(_TEST_LOCATION)
      self.assertTrue(isinstance(output, model_service_client.ModelServiceClient))

  ##_get_batch_prediction_job(self, job_client, job_name):

  def test_get_batch_prediction_job(self):
    worker_inst = vertexai_worker.VertexAIWorker(
      ##params
      {},
      ##pipeline_id: int,
      pipeline_id=1,
      ##job_id: int,
      job_id=1,
      ##logger_project: Optional[str] = None,
      logger_project=_TEST_PROJECT,
      ##logger_credentials: Optional[credentials.Credentials] = None
      logger_credentials=_make_credentials()
    )

    ## mock JobServiceClient and then inject as result of _get_vertexai_pipeline_client
    mock_job_client = mock.create_autospec(
      job_service_client.JobServiceClient, instance=True, spec_set=True)

    mock_job_client.get_batch_prediction_job.return_value = (
      gca_batch_prediction_job.BatchPredictionJob(
        name=_TEST_BATCH_PREDICTION_JOB_NAME,
        display_name=_TEST_BATCH_PREDICTION_JOB_NAME,
      )
    )

    output = worker_inst._get_batch_prediction_job(mock_job_client, _TEST_BATCH_PREDICTION_JOB_NAME)
    self.assertTrue(isinstance(output, gca_batch_prediction_job.BatchPredictionJob))

  ##_get_training_pipeline(self, pipeline_client, pipeline_name):
  def test_get_training_pipeline(self):
    worker_inst = vertexai_worker.VertexAIWorker(
      ##params
      {},
      ##pipeline_id: int,
      pipeline_id=1,
      ##job_id: int,
      job_id=1,
      ##logger_project: Optional[str] = None,
      logger_project=_TEST_PROJECT,
      ##logger_credentials: Optional[credentials.Credentials] = None
      logger_credentials=_make_credentials()
    )

    mock_pipeline_client = mock.create_autospec(
      pipeline_service_client.PipelineServiceClient, instance=True, spec_set=True)

    mock_pipeline_client.get_training_pipeline.return_value = (
      gca_training_pipeline.TrainingPipeline(
        name=_TEST_PIPELINE_RESOURCE_NAME,
      )
    )

    output = worker_inst._get_training_pipeline(mock_pipeline_client, _TEST_PIPELINE_NAME)
    self.assertTrue(isinstance(output, gca_training_pipeline.TrainingPipeline))

  @parameterized.parameters(
    {"cfg_pipeline_name": "projects/my-project/locations/us-central1/trainingPipelines/12345",
     "cfg_expected_value": "us-central1"},
  )
  ##_get_location_from_pipeline_name(self, pipeline_name):
  def test_get_location_from_pipeline_name(self, cfg_pipeline_name, cfg_expected_value):
    worker_inst = vertexai_worker.VertexAIWorker(
      ##params
      {},
      ##pipeline_id: int,
      pipeline_id=1,
      ##job_id: int,
      job_id=1,
      ##logger_project: Optional[str] = None,
      logger_project=_TEST_PROJECT,
      ##logger_credentials: Optional[credentials.Credentials] = None
      logger_credentials=_make_credentials()
    )
    output = worker_inst._get_location_from_pipeline_name(cfg_pipeline_name)
    self.assertTrue(output, cfg_expected_value)

  @parameterized.parameters(
    {"cfg_job_name": "projects/my-project/locations/us-central1/customJobs/12345",
     "cfg_expected_value": "us-central1"},
  )
  ##_get_location_from_pipeline_name(self, pipeline_name):
  def test_get_location_from_job_name(self, cfg_job_name, cfg_expected_value):
    worker_inst = vertexai_worker.VertexAIWorker(
      ##params
      {},
      ##pipeline_id: int,
      pipeline_id=1,
      ##job_id: int,
      job_id=1,
      ##logger_project: Optional[str] = None,
      logger_project=_TEST_PROJECT,
      ##logger_credentials: Optional[credentials.Credentials] = None
      logger_credentials=_make_credentials()
    )
    output = worker_inst._get_location_from_job_name(cfg_job_name)
    self.assertTrue(output, cfg_expected_value)

  ##_get_parent_resource(self, location):
  def test_get_parent_resource(self):
    worker_inst = vertexai_worker.VertexAIWorker(
      ##params
      {},
      ##pipeline_id: int,
      pipeline_id=1,
      ##job_id: int,
      job_id=1,
      ##logger_project: Optional[str] = None,
      logger_project=_TEST_PROJECT,
      ##logger_credentials: Optional[credentials.Credentials] = None
      logger_credentials=_make_credentials()
    )

    self.enter_context(
      mock.patch.object( worker_inst,'_get_project_id',
                         return_value=_TEST_PROJECT,
                         autospec=True, spec_set=True
                         )
    )

    output = worker_inst._get_parent_resource(_TEST_LOCATION)
    self.assertTrue(output, f'projects/{_TEST_PROJECT}/locations/{_TEST_LOCATION}')

  ##_wait_for_pipeline(self, pipeline):
  @parameterized.parameters(
    {"cfg_pipeline_state": gca_pipeline_state.PipelineState.PIPELINE_STATE_SUCCEEDED},
    #{"cfg_pipeline_state": gca_pipeline_state.PipelineState.PIPELINE_STATE_FAILED},
    {"cfg_pipeline_state": gca_pipeline_state.PipelineState.PIPELINE_STATE_RUNNING},
  )
  def test_wait_for_pipeline(self, cfg_pipeline_state):
    worker_inst = vertexai_worker.VertexAIWorker(
      ##params
      {},
      ##pipeline_id: int,
      pipeline_id=1,
      ##job_id: int,
      job_id=1,
      ##logger_project: Optional[str] = None,
      logger_project=_TEST_PROJECT,
      ##logger_credentials: Optional[credentials.Credentials] = None
      logger_credentials=_make_credentials()
    )
    self.enter_context(
      mock.patch(
        'time.sleep',
        side_effect=lambda delay: delay,
        autospec=True,
        spec_set=True)
    )

    mock_pipeline_client = mock.create_autospec(
      pipeline_service_client.PipelineServiceClient, instance=True, spec_set=True)

    mock_pipeline_client.get_training_pipeline.return_value = (
      gca_training_pipeline.TrainingPipeline(
        name=_TEST_PIPELINE_RESOURCE_NAME,
        state=cfg_pipeline_state,
     )
    )

    mock_pipeline = mock_pipeline_client.get_training_pipeline()
    ##if cfg_pipeline_state == gca_pipeline_state.PipelineState.PIPELINE_STATE_SUCCEEDED:

    if cfg_pipeline_state == gca_pipeline_state.PipelineState.PIPELINE_STATE_FAILED:
      with self.assertRaises(WorkerException):
        worker_inst._wait_for_pipeline(mock_pipeline)
    elif cfg_pipeline_state == gca_pipeline_state.PipelineState.PIPELINE_STATE_RUNNING:
      patched_enqueue = self.enter_context(
        mock.patch.object(
          worker_inst,
          '_enqueue',
          return_value= None,
          autospec=True,
          spec_set=True))
      worker_inst._wait_for_pipeline(mock_pipeline)
      patched_enqueue.assert_called_once()

  ##_wait_for_pipeline(self, pipeline):
  @parameterized.parameters(
    {"cfg_job_state": gca_job_state.JobState.JOB_STATE_SUCCEEDED},
    ##{"cfg_job_state": gca_job_state.JobState.JOB_STATE_FAILED},
    {"cfg_job_state": gca_job_state.JobState.JOB_STATE_RUNNING},
  )
  def test_wait_for_job(self, cfg_job_state):
    worker_inst = vertexai_worker.VertexAIWorker(
      ##params
      {},
      ##pipeline_id: int,
      pipeline_id=1,
      ##job_id: int,
      job_id=1,
      ##logger_project: Optional[str] = None,
      logger_project=_TEST_PROJECT,
      ##logger_credentials: Optional[credentials.Credentials] = None
      logger_credentials=_make_credentials()
    )
    self.enter_context(
      mock.patch(
        'time.sleep',
        side_effect=lambda delay: delay,
        autospec=True,
        spec_set=True)
    )

    mock_job_client = mock.create_autospec(
      job_service_client.JobServiceClient, instance=True, spec_set=True)

    mock_job_client.get_batch_prediction_job.return_value = (
      gca_batch_prediction_job.BatchPredictionJob(
        name=_TEST_BATCH_PREDICTION_JOB_NAME,
        display_name=_TEST_BATCH_PREDICTION_JOB_NAME,
        state=cfg_job_state,
      )
    )

    mock_job = mock_job_client.get_batch_prediction_job()


    if cfg_job_state == gca_job_state.JobState.JOB_STATE_FAILED:
      with self.assertRaises(WorkerException):
        worker_inst._wait_for_job(mock_job)
    elif cfg_job_state == gca_job_state.JobState.JOB_STATE_RUNNING:
      patched_enqueue = self.enter_context(
        mock.patch.object(
          worker_inst,
          '_enqueue',
          return_value= None,
          autospec=True,
          spec_set=True))
      worker_inst._wait_for_job(mock_job)
      patched_enqueue.assert_called_once()

  ##_clean_up_training_pipelines(self, pipeline_client, project, region):
  @parameterized.parameters(
      {"cfg_pipeline_state": gca_pipeline_state.PipelineState.PIPELINE_STATE_SUCCEEDED},
      #{"cfg_pipeline_state": gca_pipeline_state.PipelineState.PIPELINE_STATE_FAILED},
      {"cfg_pipeline_state": gca_pipeline_state.PipelineState.PIPELINE_STATE_RUNNING},
  )
  def test_clean_up_training_pipelines(self, cfg_pipeline_state):
    worker_inst = vertexai_worker.VertexAIWorker(
      ##params
      {},
      ##pipeline_id: int,
      pipeline_id=1,
      ##job_id: int,
      job_id=1,
      ##logger_project: Optional[str] = None,
      logger_project=_TEST_PROJECT,
      ##logger_credentials: Optional[credentials.Credentials] = None
      logger_credentials=_make_credentials()
    )

    mock_log = self.enter_context(mock.patch.object(worker_inst, 'log_info', autospec=True))

    mock_pipeline_client = mock.create_autospec(
      pipeline_service_client.PipelineServiceClient, instance=True, spec_set=True)


    if cfg_pipeline_state == gca_pipeline_state.PipelineState.PIPELINE_STATE_SUCCEEDED:

      mock_pipeline_client.get_training_pipeline.return_value = (
        gca_training_pipeline.TrainingPipeline(
          name=_TEST_PIPELINE_RESOURCE_NAME,
          state=cfg_pipeline_state,
        )
      )


      mock_pipeline = mock_pipeline_client.get_training_pipeline()
      ## build list of pipelines. Put two items because main code is always leaving one
      mock_pipeline_client.list_training_pipelines.return_value = [mock_pipeline, mock_pipeline]


      ## if status is SUCCEEDED ---> DELETE
      mock_pipeline_client.delete_training_pipeline.return_value = None
      worker_inst._clean_up_training_pipelines(mock_pipeline_client, _TEST_PROJECT, _TEST_LOCATION)
      ##asserts
      mock_pipeline_client.delete_training_pipeline.assert_called_once()
      mock_log.assert_called_once()

    elif cfg_pipeline_state == gca_pipeline_state.PipelineState.PIPELINE_STATE_RUNNING:

      mock_pipeline_client.get_training_pipeline.return_value = (
        gca_training_pipeline.TrainingPipeline(
          name=_TEST_PIPELINE_RESOURCE_NAME,
          state=cfg_pipeline_state,
        )
      )


      mock_pipeline = mock_pipeline_client.get_training_pipeline()
      ## build list of pipelines. Put two items because main code is always leaving one
      mock_pipeline_client.list_training_pipelines.return_value = [mock_pipeline, mock_pipeline]

      # if status is RUNNING ---> CANCEL + DELETE
      mock_pipeline_client.delete_training_pipeline.return_value = None
      mock_pipeline_client.cancel_training_pipeline.return_value = None
      worker_inst._clean_up_training_pipelines(mock_pipeline_client, _TEST_PROJECT, _TEST_LOCATION)
      ##asserts
      mock_pipeline_client.cancel_training_pipeline.assert_called_once()
      mock_pipeline_client.delete_training_pipeline.assert_called_once()
      mock_log.assert_called_once()

  @parameterized.parameters(
    {"cfg_job_state": gca_job_state.JobState.JOB_STATE_SUCCEEDED},
    {"cfg_job_state": gca_job_state.JobState.JOB_STATE_FAILED},
    {"cfg_job_state": gca_job_state.JobState.JOB_STATE_RUNNING},
  )
  def test_clean_up_batch_prediction(self, cfg_job_state):
    worker_inst = vertexai_worker.VertexAIWorker(
      ##params
      {},
      ##pipeline_id: int,
      pipeline_id=1,
      ##job_id: int,
      job_id=1,
      ##logger_project: Optional[str] = None,
      logger_project=_TEST_PROJECT,
      ##logger_credentials: Optional[credentials.Credentials] = None
      logger_credentials=_make_credentials()
    )

    mock_log = self.enter_context(mock.patch.object(worker_inst, 'log_info', autospec=True))

    mock_job_client = mock.create_autospec(
      job_service_client.JobServiceClient, instance=True, spec_set=True)


    mock_job_client.get_batch_prediction_job.return_value = (
      gca_batch_prediction_job.BatchPredictionJob(
        name=_TEST_BATCH_PREDICTION_JOB_NAME,
        display_name=_TEST_BATCH_PREDICTION_JOB_NAME,
        state=cfg_job_state,
      )
    )

    mock_job = mock_job_client.get_batch_prediction_job()
    ## build list of pipelines. Put two items because main code is always leaving one
    mock_job_client.list_batch_prediction_jobs.return_value = [mock_job, mock_job]


    if cfg_job_state == gca_job_state.JobState.JOB_STATE_SUCCEEDED:

      ## if status is SUCCEEDED ---> DELETE
      mock_job_client.delete_batch_prediction_job.return_value = None
      worker_inst._clean_up_batch_predictions(mock_job_client, _TEST_PROJECT, _TEST_LOCATION)
      ##asserts
      mock_job_client.delete_batch_prediction_job.assert_called_once()
      mock_log.assert_called_once()

    elif cfg_job_state == gca_job_state.JobState.JOB_STATE_RUNNING:

      # if status is RUNNING ---> CANCEL + DELETE
      mock_job_client.delete_batch_prediction_job.return_value = None
      mock_job_client.cancel_batch_prediction_job.return_value = None
      worker_inst._clean_up_batch_predictions(mock_job_client, _TEST_PROJECT, _TEST_LOCATION)
      ##asserts
      mock_job_client.cancel_batch_prediction_job.assert_called_once()
      mock_job_client.delete_batch_prediction_job.assert_called_once()
      mock_log.assert_called_once()








## _clean_up_batch_predictions(self, job_client, project, region):

if __name__ == '__main__':
  absltest.main()
