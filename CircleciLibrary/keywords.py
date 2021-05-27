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
from robot.api.deco import library, keyword
from CircleciLibrary.model import Project, Workflow, Pipeline, WorkflowList
from pycircleci.api import Api, API_BASE_URL


class WorkflowError(Exception):
    """
    this exception will be raised if the workflow is not completed successfully
    """


@library
class CircleciLibraryKeywords:
    """
    circleci keywords
    """
    def __init__(self, api_token, base_url=API_BASE_URL):
        """
        :param api_token: circleci api token
        :param base_url: circleci base url (default: pycircleci.api.API_BASE_URL)
        """
        self.api = Api(api_token, url=base_url)

    @keyword
    def create_project(self, vcs: str, organisation: str, repository: str) -> Project:
        """
        create a project object

        :param vcs: vcs type
        :param organisation: project organisation
        :param repository: name of the repository
        :return: Project object
        """
        return Project(
            vcs=vcs,
            organisation=organisation,
            repository=repository
        )

    @keyword
    def trigger_pipeline(
            self,
            project: Project,
            branch: str = None,
            tag: str = None,
            parameters: dict = {}
    ) -> Pipeline:
        """
        Triggers a circleci pipeline

        :param project: the circleci project
        :param branch: the branch to build
            Defaults to None. Cannot be used with the ``tag`` parameter.
        :param tag: the tag to build
            Defaults to None. Cannot be used with the ``branch`` parameter.
        :param parameters:  additional pipeline parameters (default: {})
        :return: Pipeline object
        """
        response = self.api.trigger_pipeline(
                username=project.organisation,
                project=project.repository,
                branch=branch,
                tag=tag,
                vcs_type=project.vcs,
                params=parameters
        )
        return Pipeline.from_json(response)

    @keyword
    def get_pipeline(self, pipeline_id) -> Pipeline:
        """
        Get the information for a given pipeline
        :param pipeline_id: the id of a circleci pipeline
        :return: Pipeline object
        """
        return Pipeline.from_json(self.api.get_pipeline(pipeline_id))

    @keyword
    def get_workflows(self, pipeline: Pipeline) -> WorkflowList:
        """
        Get the information for all workflow of a given pipeline

        :param pipeline: circleci pipeline object
        :return: list of workflows object
        """
        response = self.api.get_pipeline_workflow(pipeline.id)
        workflows = [Workflow.from_json(i) for i in response['items']]
        return WorkflowList.from_list(workflows)

    @keyword
    def workflows_completed(self, pipeline: Pipeline) -> bool:
        """
        Return True if all workflows of the given pipeline complete

        :param pipeline: circleci pipeline object
        :return: True if all workflows of this pipeline are complete
        """
        workflows = self.get_workflows(pipeline)
        return workflows.completed()

    @keyword
    def workflows_completed_with_status(self, pipeline: Pipeline, status: Workflow.Status) -> bool:
        """
        Return True if all workflows of the given pipeline completed with the desired status

        :param pipeline: circleci pipeline object
        :param status: desired status
        :return: True if all workflows of this pipeline are complete with the desired status
        """
        workflows = self.get_workflows(pipeline)
        return workflows.completed() and workflows.overall_status(status)

    @keyword
    def check_if_workflows_completed_with_status(self, pipeline: Pipeline, status: Workflow.Status):
        """
        Check if all workflows of the given pipeline completed with the desired status

        :param pipeline: circleci pipeline object
        :param status: desired status
        :raise: WorkflowError if not all workflows of this pipeline are complete with the desired status
        """
        if not self.workflows_completed_with_status(pipeline, status):
            raise WorkflowError(f"Workflows not completed with status {status.name} for pipeline: {pipeline}")

