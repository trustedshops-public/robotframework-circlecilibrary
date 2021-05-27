#!/usr/bin/env python3
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
from setuptools import setup, find_packages
import unittest
import re
from os.path import join, dirname, abspath

SETUP_DIR = dirname(abspath(__file__))

with open(join(SETUP_DIR, 'CircleciLibrary', '__init__.py')) as f:
    VERSION = re.search("\n__version__\s=\s'(.*)'", f.read()).group(1)


def project_test_suite():
    test_loader = unittest.TestLoader()
    test_suite = test_loader.discover('tests', pattern='*_test.py')
    return test_suite


with open('README.md') as f:
    long_description = f.read()


setup(
    name='robotframework-circlecilibrary',
    description='A robotframework extension to run circleci pipelines',
    long_description=long_description,
    long_description_content_type="text/markdown",
    version=VERSION,
    include_package_data=True,
    author="Thomas Volk",
    author_email="thomas.volk@trustedshops.com",
    classifiers=[
        "Programming Language :: Python :: 3.9",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
        "Topic :: Software Development :: Testing",
        "Topic :: Software Development :: Testing :: Acceptance",
        "Framework :: Robot Framework",
    ],
    packages=find_packages(exclude=("tests",)),
    test_suite="setup.project_test_suite",
    install_requires=[
      'pycircleci>=0.3.2',
      'robotframework>=4.0.0'
    ],
    url='https://github.com/trustedshops-public/robotframework-circlecilibrary',
    license='Apache License 2.0',
    platforms='any',
    python_requires='>3.9.0'
)
