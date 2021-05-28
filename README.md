
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
