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
from dataclasses import dataclass
from datetime import datetime
from enum import Enum, unique


@dataclass
class Project:
    """circleci project"""
    @staticmethod
    def from_json(d: dict):
        return Project(
            vcs_type=d['vcs_type'],
            username=d['username'],
            reponame=d['reponame']
        )

    username: str
    reponame: str
    vcs_type: str

    def __init__(self, vcs_type: str, username: str, reponame: str):
        self.vcs_type = vcs_type
        self.username = username
        self.reponame = reponame


@dataclass
class Pipeline:
    """circleci pipeline object"""
    @staticmethod
    def parse_datetime(dt_str: str) -> datetime:
        if dt_str is None:
            return None
        return datetime.strptime(dt_str, '%Y-%m-%dT%H:%M:%S.%f%z')

    @dataclass
    class Error:
        """error information of a pipeline"""
        @staticmethod
        def from_json(d: dict):
            return Pipeline.Error(d['type'], d['message'])

        type: str
        message: str

        def __init__(self, error_type: str, message: str):
            self.type = error_type
            self.message = message

    @dataclass
    class Vcs:
        """vcs information of a pipeline"""
        @staticmethod
        def from_json(d: dict):
            return Pipeline.Vcs(
                provider_name=d['provider_name'],
                target_repository_url=d['target_repository_url'],
                branch=d.get('branch'),
                tag=d.get('tag')
            )

        provider_name: str
        target_repository_url: str
        branch: str
        tag: str

    def __int__(
            self,
            provider_name: str,
            target_repository_url: str,
            branch: str,
            tag: str
    ):
        self.provider_name = provider_name
        self.target_repository_url = target_repository_url
        self.branch = branch
        self.tag = tag

    @staticmethod
    def from_json(d: dict):
        created = Pipeline.parse_datetime(d['created_at'])
        updated_at = Pipeline.parse_datetime(d.get('updated_at'))
        errors = [Pipeline.Error.from_json(j) for j in d.get('errors', [])]
        vcs = Pipeline.Vcs.from_json(d['vcs']) if 'vcs' in d.keys() else None
        return Pipeline(
            pipeline_id=d['id'],
            number=d['number'],
            state=d['state'],
            created_at=created,
            updated_at=updated_at,
            errors=errors,
            vcs=vcs
        )

    id: str
    number: int
    state: str
    created_at: datetime
    updated_at: datetime
    errors: list[Error]
    vcs: Vcs

    def __init__(
            self,
            pipeline_id: str,
            number: int,
            state: str,
            created_at: datetime,
            updated_at: datetime,
            errors: list[Error],
            vcs: Vcs
    ):
        self.number = number
        self.state = state
        self.id = pipeline_id
        self.created_at = created_at
        self.updated_at = updated_at
        self.errors = errors
        self.vcs = vcs


@dataclass
class Workflow:
    """circleci workflow object"""
    @unique
    class Status(Enum):
        """status which a circleci workflow could have"""
        SUCCESS = 'success'
        RUNNING = 'running'
        ON_HOLD = 'on_hold'
        NOT_RUN = 'not_run'
        FAILED = 'failed'
        ERROR = 'error'
        FAILING = 'failing'
        CANCELLED = 'canceled'
        UNAUTHORIZED = 'unauthorized'

    id: str
    name: str
    pipeline_id: str
    pipeline_number: str
    project_slug: str
    status: Status
    started_by: str
    created_at: datetime
    stopped_at: datetime

    @staticmethod
    def from_json(d: dict):
        def parse_datetime(dt_str: str):
            if dt_str is None:
                return None
            return datetime.strptime(dt_str, '%Y-%m-%dT%H:%M:%S%z')

        created = parse_datetime(d['created_at'])
        stopped = parse_datetime(d['stopped_at'])
        return Workflow(
            workflow_id=d['id'],
            name=d['name'],
            pipeline_id=d['pipeline_id'],
            pipeline_number=d['pipeline_number'],
            project_slug=d['project_slug'],
            status=Workflow.Status(d['status']),
            started_by=d['started_by'],
            created_at=created,
            stopped_at=stopped
        )

    def __init__(
            self,
            workflow_id: str,
            name: str,
            pipeline_id: str,
            pipeline_number: str,
            project_slug: str,
            status: str,
            started_by: str,
            created_at: datetime,
            stopped_at: datetime = None
    ):
        self.id = workflow_id
        self.name = name
        self.pipeline_id = pipeline_id
        self.pipeline_number = pipeline_number
        self.project_slug = project_slug
        self.status = status
        self.started_by = started_by
        self.created_at = created_at
        self.stopped_at = stopped_at

    def in_progress(self) -> bool:
        return self.stopped_at is None


class WorkflowList(list[Workflow]):
    """a list of circleci workflow objects"""
    @staticmethod
    def from_list(l: list):
        wl = WorkflowList()
        wl.extend(l)
        return wl

    def completed(self) -> bool:
        """
        :return: True if all workflows of this pipeline are complete
        """
        if len(self) == 0:
            return False
        in_progress = [w for w in self if w.in_progress()]
        return len(in_progress) == 0

    def overall_status(self, status: Workflow.Status):
        """
        :param status: desired status
        :return: True if all workflows have the given status
        """
        success_workflows = [w for w in self if w.status == status]
        return len(self) == len(success_workflows)
