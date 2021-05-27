[![CircleCI](https://circleci.com/gh/trustedshops/robotframework-circlecilibrary.svg?style=svg&circle-token=69de5d6ada315347ab0243a5510919027686dfc0)](https://app.circleci.com/pipelines/github/trustedshops/robotframework-circlecilibrary)

# robotframework-circlecilibrary

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
Library           CircleciLibrary  %{CIRCLECI_API_TOKEN}

*** Test Cases ***
Trigger a circleci pipeline
    ${project}                       Create Project         github        my-org      my-project
    ${pipeline}                      Trigger Pipeline       ${project}    tag=1.0.0
    Wait Until Keyword Succeeds      2m                     2s
                                     ...                    Check If Workflows Completed With Status
                                                            ...    ${pipeline}    status=success
```

## Development

Run the setup to install all dependencies.
```sh
./setup.py install
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

## License

robotframework-circlecilibrary is open source software provided under the [Apache License
2.0](http://apache.org/licenses/LICENSE-2.0)
