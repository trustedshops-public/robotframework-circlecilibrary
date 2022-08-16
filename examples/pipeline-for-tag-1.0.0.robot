
*** Settings ***
Documentation     Handle circleci pipeline example
Library           CircleciLibrary  api_token=%{CIRCLECI_API_TOKEN}

*** Test Cases ***
Trigger a circleci pipeline
    ${project}                                Get Project         robotframework-circlecilibrary-test-project
    ${pipeline}                               Trigger Pipeline
                                              ...                 ${project}    tag=1.0.0
    Wait Until Keyword Succeeds               5m                  2s
                                              ...                 All Workflows Should Be Stopped    ${pipeline}
    All Workflows Should Have The Status      ${pipeline}         success