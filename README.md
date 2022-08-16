
# robotframework-circlecilibrary

[![GitHub License](https://img.shields.io/badge/license-MIT-lightgrey.svg)](https://github.com/trustedshops-public/circleci-orb-semantic-release/blob/main/LICENSE)
[![pre-commit](https://img.shields.io/badge/%E2%9A%93%20%20pre--commit-enabled-success)](https://pre-commit.com/)
[![CircleCI](https://circleci.com/gh/trustedshops-public/robotframework-circlecilibrary/tree/main.svg?style=shield)](https://circleci.com/gh/trustedshops-public/robotframework-circlecilibrary/tree/main)
[![PyPI version](https://badge.fury.io/py/robotframework-circlecilibrary.svg)](https://pypi.org/project/robotframework-circlecilibrary)

robotframework-circlecilibrary is an extension library for the [robotframework](https://robotframework.org/)
to trigger and mange circleci pipelines.

## Usage

Install robotframework-circlecilibrary via pip:

```sh
pip install --upgrade robotframework-circlecilibrary
```

Now you can trigger a pipeline and wait until it is complete:

```robotframework
*** Settings ***
Documentation     Handle circleci pipeline example
Library           CircleciLibrary  api_token=%{CIRCLECI_API_TOKEN}

*** Test Cases ***
Trigger a circleci pipeline
    ${project}                                Get Project         my-project
    ${pipeline}                               Trigger Pipeline
                                              ...                 ${project}    tag=2.0.1
    Wait Until Keyword Succeeds               5m                  2s
                                              ...                 All Workflows Should Be Stopped    ${pipeline}
    All Workflows Should Have The Status      ${pipeline}         success
```

### Tracing

robotframework-circlecilibrary will log all return values received from the circleci api:

    robot --loglevel=TRACE pipeline.robot

## Releases

* 0.1.3 - bugfix for circleci get workflows for pipeline, add tracing
* 0.1.2 - make library compatible for python >=3.9.0
* 0.1.1 - fix documentation
* 0.1.0 - initial release

## Development

Run the setup to install all dependencies.
```sh
pip install .
```


### Build and Run

#### Run Tests

To run the tests you need to install tox in the first place:

```sh
pip3 install tox
```

After that you can run the test via tox:

```sh
tox
```

## Deployment

1. Increase version number in CircleciLibrary/\_\_init\_\_.py.
2. Create a tag in GitHub for the version number.
3. Create pip account configuration file in $HOME/.pypirc:
```
[distutils]
    index-servers =
    pip-test-account
    pip-prod-account

[pip-test-account]
    repository = https://test.pypi.org/legacy/
    username = __token__
    password = <generate your api token on https://test.pypi.org>

[pip-prod-account]
    repository = https://upload.pypi.org/legacy/
    username = __token__
    password = <generate your api token on https://pypi.org>
```
4. Try a test deployment:
```make test_deploy```
5. If successful, deploy:
```make deploy```
