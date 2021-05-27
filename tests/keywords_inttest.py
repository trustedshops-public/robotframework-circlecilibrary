"""
Copyright 2021 Trusted Shops

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

   http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""
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
