# -*- coding: utf-8 -*-
from setuptools import find_packages, setup
import sys
import os


withcoverage = os.environ.get("WITH_COVERAGE")

setup(
    name="aimmo-game-worker-simulation-test",
    version="0.0.1a0",
    packages=["simulation"],
    include_package_data=True,
    install_requires=["flask", "requests"],
    tests_require=["httmock", "mock"],
    test_suite="tests",
    zip_safe=False,
)
