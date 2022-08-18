import os
from keywords import KeywordsTestCase


def _from_env(var_name):
    value = os.environ.get(var_name)
    if value is None:
        raise RuntimeError(f"Environment variable {var_name} is missing!")
    return value


class KeywordsIntegrationTest(KeywordsTestCase):
    def setUp(self):
        self.api_token = _from_env('CIRCLECI_API_TOKEN')

    def test_trigger_pipeline_with_branch_main(self):
        self._test_trigger_pipeline_with_branch_main()

    def test_trigger_pipeline_with_tag(self):
        self._test_trigger_pipeline_with_tag()

    def test_get_project(self):
        self._test_get_project()
