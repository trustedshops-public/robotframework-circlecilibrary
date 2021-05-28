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


class WorkflowRunningError(Exception):
    """
    this exception will be raised if the workflow is still running
    """


class WorkflowStatusError(Exception):
    """
    this exception will be raised if the workflow does not have the desired status
    """


class ProjectNotFoundError(Exception):
    """
    this exception will be raised if a project was not found by the given criteria
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
    def define_project(self, vcs_type: str, username: str, reponame: str) -> Project:
        """
        creates a project object

        :param vcs_type: vcs type
        :param username: project organisation
        :param reponame: name of the repository
        :return: Project object
        """
        return Project(
            vcs_type=vcs_type,
            username=username,
            reponame=reponame
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
                username=project.username,
                project=project.reponame,
                branch=branch,
                tag=tag,
                vcs_type=project.vcs_type,
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
    def all_workflows_stopped(self, pipeline: Pipeline) -> bool:
        """
        Return True if all workflows of the given pipeline completed

        :param pipeline: circleci pipeline object
        :return: True if all workflows of this pipeline are complete
        """
        workflows = self.get_workflows(pipeline)
        return workflows.completed()

    @keyword
    def all_workflows_should_be_stopped(self, pipeline: Pipeline):
        """
        Check if all workflows of the given pipeline stopped

        :param pipeline: circleci pipeline object
        :raise: WorkflowRunningError if not all workflows of this pipeline are stopped
        """
        if not self.all_workflows_stopped(pipeline):
            raise WorkflowRunningError(f"Workflows still running for pipeline: {pipeline}")

    @keyword
    def all_workflows_have_status(self, pipeline: Pipeline, status: Workflow.Status):
        """
        :return: True if all workflows have the desired status
        """
        for w in self.get_workflows(pipeline):
            if w.status != status:
                return False
        return True

    @keyword
    def all_workflows_should_have_the_status(self, pipeline: Pipeline, status: Workflow.Status):
        """
        Check if all workflows have the desired status

        :param pipeline: circleci pipeline object
        :param status: desired workflow status
        :raise: WorkflowStatusError if not all workflows have the desired status
        """
        if not self.all_workflows_have_status(pipeline, status):
            raise WorkflowStatusError(f"Workflows do not have the status {status.name} for pipeline: {pipeline}")

    def _get_projects(self):
        for p in self.api.get_projects():
            yield Project.from_json(p)

    @keyword
    def get_projects(self):
        """
        :return: all projects of the current user
        """
        return list(self._get_projects())

    @keyword
    def get_project(self, name):
        """
        returns the desired project of the current user

        :param name: name of the desired project
        :return: the desired project of the current user
        :raise: ProjectNotFoundError if no project was found for the given name
        """
        for p in self._get_projects():
            if p.reponame == name:
                return p
        raise ProjectNotFoundError(f"project {name} was not found in the projects list of the current user")
