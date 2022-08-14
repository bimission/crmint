from unittest import mock

from absl.testing import absltest
from absl.testing import parameterized


from jobs.workers.vertexai import vertexai_tabular_trainer


_TEST_PROJECT = "test-project"
_TEST_LOCATION = "us-central1"

_TEST_VERETXAI_MODEL_NAME = "test-model"

def _make_credentials():
  creds = mock.create_autospec(
    credentials.Credentials, instance=True, spec_set=True)
  return creds

class VertexAITabularTrainerTest(parameterized.TestCase):


  @parameterized.parameters(
    {
      'clean_up': True,
      'vertexai_model_name': _TEST_VERETXAI_MODEL_NAME
    }
  )
  def test_create_veretxai_dataset(self,
          cfg_clan_up,
          cfg_vertexai_model_name
         ):

    worker_inst = jobs.workers.vertexai.VertexAITabularTrainer(
      ##params
      {
        'clean_up': 0,
        'vertexai_model_name': 0,
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


if __name__ == '__main__':
  absltest.main()
