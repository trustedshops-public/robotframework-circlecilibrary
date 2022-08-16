#!/usr/bin/env python3
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

with open("requirements.txt", "r") as requirements_file:
    requirements = requirements_file.readlines()

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
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Software Development :: Testing",
        "Topic :: Software Development :: Testing :: Acceptance",
        "Framework :: Robot Framework",
    ],
    packages=find_packages(exclude=("tests",)),
    test_suite="setup.project_test_suite",
    install_requires=requirements,
    url='https://github.com/trustedshops-public/robotframework-circlecilibrary',
    license='MIT License',
    platforms='any',
    python_requires='>=3.9.0'
)
