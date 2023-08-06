#!/usr/bin/env python3

import os
import re
import sys
from setuptools import find_packages, setup


def read(*parts):
    """Read file."""
    filename = os.path.join(os.path.abspath(os.path.dirname(__file__)), *parts)
    sys.stdout.write(filename)
    with open(filename, encoding="utf-8", mode="rt") as fp:
        return fp.read()


with open("Readme.md") as readme_file:
    readme = readme_file.read()

setup(
    author="Sky Moore",
    author_email="sky.moore@isostech.com",
    classifiers=[
        "Natural Language :: English",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3 :: Only"
    ],
    description="Test your cloud automation environment for Isos Technology.",
    include_package_data=True,
    python_requires=">=3.7",
    install_requires=["requests>=2.22.0",
                      "atlassian-python-api>=1.15.6",
                      "console-menu>=0.6.0"],
    keywords=["Isos Technology", "Isos", "Atlassian", "Atlassian Cloud"],
    long_description_content_type="text/markdown",
    long_description=readme,
    name="isos-environment-test",
    packages=find_packages(include=["isos-env-test"]),
    url="https://git.isostech.com/scm/act/python3-cloud-automation-env-test.git",
    version="0.0.2",
    zip_safe=False,
)
