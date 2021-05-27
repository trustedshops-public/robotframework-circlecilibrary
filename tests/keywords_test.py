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
from unittest.mock import Mock, patch
from keywords import KeywordsTestCase
from CircleciLibrary import CircleciLibrary
from CircleciLibrary.model import Pipeline, Workflow


class KeywordsUnitTest(KeywordsTestCase):
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

    @patch('CircleciLibrary.keywords.Api')
    def test_trigger_pipeline(self, api_constructor_mock):
        api_mock = Mock()
        api_constructor_mock.return_value = api_mock

        pipeline = {
            'number': 129,
            'state': 'pending',
            'id': 'E57868E8-9533-4625-AD83-F2AB2ABB70BD',
            'created_at': '2021-05-21T13:44:31.668Z'
        }
        api_mock.trigger_pipeline.return_value = pipeline

        api_mock.get_pipeline = Mock()
        api_mock.get_pipeline.return_value = {
                'id': 'E57868E8-9533-4625-AD83-F2AB2ABB70BD',
                'errors': [],
                'project_slug': 'gh/trustedshops/circleci_api_test_dummy',
                'updated_at': '2021-05-21T13:44:31.668Z',
                'number': 129,
                'state': 'created',
                'created_at': '2021-05-21T13:44:31.668Z',
                'vcs': {
                    'origin_repository_url': 'https://github.com/trustedshops/robotframework_circleci_test_dummy',
                    'target_repository_url': 'https://github.com/trustedshops/robotframework_circleci_test_dummy',
                    'revision': '87457315102ea6aab36c3c2ee7b04dd75af195e1',
                    'provider_name': 'GitHub',
                    'branch': 'main'
                }
            }

        def workflows(stopped: bool, status: str):
            return {
                'items': [
                    {
                        'pipeline_id': 'E57868E8-9533-4625-AD83-F2AB2ABB70BD',
                        'id': '0A3EF846-8A63-4851-98E2-055486715DEF',
                        'name': 'build',
                        'project_slug': 'gh/trustedshops/circleci_api_test_dummy',
                        'status': status,
                        'started_by': 'DA2E42D1-DD08-4D4F-9E78-1B0C3C4D3183',
                        'pipeline_number': 134,
                        'created_at': '2021-05-21T14:39:08Z',
                        'stopped_at': '2021-05-21T14:40:08Z' if stopped else None
                    }
                ]
            }

        api_mock.get_pipeline_workflow = Mock()
        api_mock.get_pipeline_workflow.side_effect = [
            workflows(stopped=False, status='running'),
            workflows(stopped=False, status='running'),
            workflows(stopped=False, status='running'),
            workflows(stopped=True, status='success'),
            workflows(stopped=True, status='success'),
            workflows(stopped=True, status='success')
        ]

        self._test_trigger_pipeline_with_branch_main()

        circleci = CircleciLibrary(self.api_token)
        pipeline = Pipeline.from_json(pipeline)
        self.assertFalse(circleci.workflows_completed(pipeline))
        self.assertTrue(circleci.workflows_completed_with_status(pipeline, Workflow.Status.SUCCESS))
        circleci.check_if_workflows_completed_with_status(pipeline, Workflow.Status.SUCCESS)

    @patch('CircleciLibrary.keywords.Api')
    def test_trigger_pipeline_with_tag(self, api_constructor_mock):
        api_mock = Mock()
        api_constructor_mock.return_value = api_mock

        api_mock.trigger_pipeline.return_value = {
            'number': 129,
            'state': 'pending',
            'id': 'E57868E8-9533-4625-AD83-F2AB2ABB70BD',
            'created_at': '2021-05-21T13:44:31.668Z'
        }

        api_mock.get_pipeline.return_value = {
                'id': 'E57868E8-9533-4625-AD83-F2AB2ABB70BD',
                'errors': [],
                'project_slug': 'gh/trustedshops/circleci_api_test_dummy',
                'updated_at': '2021-05-21T13:44:31.668Z',
                'number': 129,
                'state': 'created',
                'created_at': '2021-05-21T13:44:31.668Z',
                'vcs': {
                    'origin_repository_url': 'https://github.com/trustedshops/robotframework_circleci_test_dummy',
                    'target_repository_url': 'https://github.com/trustedshops/robotframework_circleci_test_dummy',
                    'revision': '87457315102ea6aab36c3c2ee7b04dd75af195e1',
                    'provider_name': 'GitHub',
                    'tag': '1.0.2'
                }
            }

        self._test_trigger_pipeline_with_tag()
