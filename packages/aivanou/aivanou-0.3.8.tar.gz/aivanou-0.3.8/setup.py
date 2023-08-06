#!/usr/bin/env python3

# Copyright (c) Facebook, Inc. and its affiliates.
# All rights reserved.
#
# This source code is licensed under the BSD-style license found in the
# LICENSE file in the root directory of this source tree.

import os
import re
import sys
import subprocess

from setuptools import find_packages, setup
from setuptools.command.install import install


class VerifyVersionCommand(install):
    """Custom command to verify that the git tag matches our version"""
    description = 'verify that the git tag matches our version'

    def run(self):
        if 'BASE_BUILD_VERSION' not in os.environ:
            info = "Setup BASE_BUILD_VERSION variable to run verify command"
            sys.exit(info)

        base_version = os.getenv('BASE_BUILD_VERSION')
        if base_version[0] == 'v':
            base_version = base_version[1:]
        file_version = f"{get_version()}"

        if base_version != file_version:
            info = "Git tag: {0} does not match the version: {1}".format(
                base_version, file_version
            )
            sys.exit(info)


def get_version():
    # get version string from version.py
    version = open('version.txt', 'r').read().strip()
    sha = 'Unknown'
    try:
        cwd = os.path.dirname(os.path.abspath(__file__))
        sha = subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=cwd).decode('ascii').strip()
    except Exception:
        pass

    if 'BASE_BUILD_VERSION' not in os.environ and sha != 'Unknown':
        version = f"{version}+{sha[:7]}"

    return version


if __name__ == "__main__":
    if sys.version_info < (3, 6):
        sys.exit("python >= 3.6 required")

    with open("README.md", encoding="utf8") as f:
        readme = f.read()

    with open("requirements.txt") as f:
        reqs = f.read()

    version = get_version()
    print("-- Building version: " + version)

    setup(
        # Metadata
        name="aivanou",
        version=version,
        author="Aivanou",
        author_email="csivanou@gmail.com",
        description="Test project",
        long_description=readme,
        long_description_content_type="text/markdown",
        url="https://github.com/tierex/algorithms",
        license="BSD-3",
        keywords=["test"],
        python_requires=">=3.6",
        install_requires=reqs.strip().split("\n"),
        include_package_data=True,
        packages=find_packages(exclude=("test", "test.*")),
        test_suite="test.suites.unittests",
        # PyPI package information.
        classifiers=[
        ],
        cmdclass={
            'verify': VerifyVersionCommand,
        }
    )
