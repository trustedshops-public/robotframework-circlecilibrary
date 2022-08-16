from unittest import TestCase
from CircleciLibrary.keywords import ProjectNotFoundError
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

        circleci.all_workflows_stopped(pipeline)

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

    def _test_get_project(self):
        circleci = CircleciLibrary(self.api_token)
        with self.assertRaises(ProjectNotFoundError):
            circleci.get_project('NOT_FOUND-71C5FE3D-B2E2-4D2D-9271-6D6B292B576B')
        return circleci.get_project('robotframework_circleci_test_dummy')