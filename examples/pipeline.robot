# Copyright 2021 Trusted Shops

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#    http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

*** Settings ***
Documentation     Handle circleci pipeline example
Library           CircleciLibrary  api_token=%{CIRCLECI_API_TOKEN}

*** Test Cases ***
Trigger a circleci pipeline
    ${project}                       Create Project         github        trustedshops
                                     ...                    robotframework_circleci_test_dummy
    ${pipeline}                      Trigger Pipeline       ${project}    tag=pipeline.robot
    Wait Until Keyword Succeeds      2m                     2s
                                     ...                    Check If Workflows Completed With Status
                                                            ...    ${pipeline}    status=success
