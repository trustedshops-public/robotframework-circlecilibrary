from unittest.mock import Mock, patch
from CircleciLibrary.keywords import WorkflowRunningError, WorkflowStatusError
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

    def workflows(self, stopped: bool, status: str):
            return {
                'items': [
                    self.workflow_item(stopped, status)
                ]
            }

    def workflow_item(self, stopped: bool, status: str):
        return {
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

    @patch('CircleciLibrary.keywords.Api')
    def test_get_workflows(self, api_constructor_mock):
        api_mock = Mock()
        api_constructor_mock.return_value = api_mock

        api_mock.get_pipeline_workflow = Mock()
        api_mock.get_pipeline_workflow.side_effect = [
            [ self.workflow_item(stopped=True, status='success') ],
            self.workflows(stopped=True, status='success'),
            "Wrong Object"
        ]

        pipeline = Pipeline(pipeline_id="ID",
            number=1,
            state="",
            created_at=None,
            updated_at=None,
            errors=[],
            vcs=None)

        circleci = CircleciLibrary(self.api_token)
        response = circleci.get_workflows(pipeline)
        self.assertEqual('0A3EF846-8A63-4851-98E2-055486715DEF', response[0].id)
        response = circleci.get_workflows(pipeline)
        self.assertEqual('0A3EF846-8A63-4851-98E2-055486715DEF', response[0].id)
        self.assertRaises(RuntimeError, circleci.get_workflows, pipeline)

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

        api_mock.get_pipeline_workflow = Mock()
        api_mock.get_pipeline_workflow.side_effect = [
            [ self.workflow_item(stopped=False, status='running') ],
            self.workflows(stopped=False, status='running'),
            self.workflows(stopped=False, status='running'),
            self.workflows(stopped=False, status='running'),
            self.workflows(stopped=False, status='running'),
            self.workflows(stopped=False, status='running'),
            self.workflows(stopped=False, status='running'),
            self.workflows(stopped=True, status='success'),
            self.workflows(stopped=True, status='success'),
            self.workflows(stopped=True, status='success')
        ]

        self._test_trigger_pipeline_with_branch_main()

        circleci = CircleciLibrary(self.api_token)
        pipeline = Pipeline.from_json(pipeline)
        self.assertFalse(circleci.all_workflows_stopped(pipeline))
        self.assertTrue(circleci.all_workflows_have_status(pipeline, Workflow.Status.RUNNING))
        self.assertFalse(circleci.all_workflows_have_status(pipeline, Workflow.Status.SUCCESS))
        with self.assertRaises(WorkflowStatusError):
            circleci.all_workflows_should_have_the_status(pipeline, Workflow.Status.SUCCESS)
        with self.assertRaises(WorkflowRunningError):
            circleci.all_workflows_should_be_stopped(pipeline)
        circleci.all_workflows_should_have_the_status(pipeline, Workflow.Status.SUCCESS)
        circleci.all_workflows_should_be_stopped(pipeline)

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

    @patch('CircleciLibrary.keywords.Api')
    def test_get_project(self, api_constructor_mock):
        api_mock = Mock()
        api_constructor_mock.return_value = api_mock
        api_mock.get_projects.return_value = [
            {
                'branches': [],
                'oss': False,
                'reponame': 'robotframework_circleci_test_dummy',
                'username': 'trustedshops',
                'has_usable_key': False,
                'vcs_type': 'github',
                'language': None,
                'vcs_url': 'https://github.com/trustedshops/robotframework_circleci_test_dummy',
                'following': False,
                'default_branch': 'main'
            },
            {
                'branches': [],
                'oss': False,
                'reponame': 'repo2',
                'username': 'my-org',
                'has_usable_key': False,
                'vcs_type': 'github',
                'language': None,
                'vcs_url': 'https://github.com/my-org/repo-1',
                'following': False,
                'default_branch': 'main'
            },
            {
                'branches': [],
                'oss': False,
                'reponame': 'repo3',
                'username': 'my-org',
                'has_usable_key': False,
                'vcs_type': 'github',
                'language': None,
                'vcs_url': 'https://github.com/my-org/repo-1',
                'following': False,
                'default_branch': 'main'
            }
        ]
        project = self._test_get_project()
        self.assertEqual('robotframework_circleci_test_dummy', project.reponame)
        self.assertEqual('trustedshops', project.username)
        self.assertEqual('github', project.vcs_type)