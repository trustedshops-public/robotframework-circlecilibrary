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
from unittest import TestCase
from CircleciLibrary.model import Project
from CircleciLibrary import CircleciLibrary


class KeywordsTestCase(TestCase):
    api_token = "MOCK"
    test_project = Project('github', 'trustedshops', 'robotframework_circleci_test_dummy')

    def __validate_pipeline_reference(self, pipeline):
        self.assertIsNotNone(pipeline)
        self.assertIsNotNone(pipeline.created_at)
        self.assertIsNotNone(pipeline.state)
        self.assertIsNotNone(pipeline.number)
        self.assertIsNotNone(pipeline.id)

    def __validate_workflow(self, workflow):
        self.assertIsNotNone(workflow)
        self.assertIsNotNone(workflow.id)
        self.assertIsNotNone(workflow.name)
        self.assertIsNotNone(workflow.status)
        self.assertIsNotNone(workflow.created_at)
        self.assertIsNotNone(workflow.pipeline_number)
        self.assertIsNotNone(workflow.pipeline_id)
        self.assertIsNotNone(workflow.project_slug)

    def _test_trigger_pipeline_with_branch_main(self):
        circleci = CircleciLibrary(self.api_token)
        pipeline = circleci.trigger_pipeline(self.test_project)
        self.__validate_pipeline_reference(pipeline)

        # reload pipeline
        pipeline = circleci.get_pipeline(pipeline.id)
        self.assertIsNone(pipeline.vcs.tag)
        self.assertEqual('main', pipeline.vcs.branch)

        workflows = circleci.get_workflows(pipeline)
        self.assertEqual(1, len(workflows))
        for w in workflows:
            self.__validate_workflow(w)

        circleci.workflows_completed(pipeline)

    def _test_trigger_pipeline_with_tag(self):
        circleci = CircleciLibrary(self.api_token)
        pipeline = circleci.trigger_pipeline(self.test_project, tag='1.0.2')
        self.__validate_pipeline_reference(pipeline)

        # reload pipeline
        pipeline = circleci.get_pipeline(pipeline.id)
        self.assertEqual('1.0.2', pipeline.vcs.tag)
        self.assertIsNone(pipeline.vcs.branch)
        self.assertEqual('https://github.com/trustedshops/robotframework_circleci_test_dummy', pipeline.vcs.target_repository_url)
        self.assertEqual('GitHub', pipeline.vcs.provider_name)
