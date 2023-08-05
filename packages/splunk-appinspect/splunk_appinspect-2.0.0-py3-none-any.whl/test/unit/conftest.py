# Copyright 2016 Splunk Inc. All rights reserved.

# Python Standard Libraries
import os
import six
# Third-Party Libraries
# N/A
# Custom Libraries
from . import testutils

packages_dir = os.path.join(os.path.split(__file__)[0], 'packages')


def pytest_collect_file(parent, path):
    if path.ext == ".csv" and path.basename.startswith("test"):
        # to avoid collecting all test cases during development,
        # developer can specify a specific csv file using the `APPINSPECT_TEST` environment variable
        # for example,
        if path.dirname.endswith("py3_test_scenarios"):
            if not six.PY2:
                return collect_file(parent, path)
        elif path.dirname.endswith("py2_test_scenarios"):
            if six.PY2:
                return collect_file(parent, path)
        else:
            return collect_file(parent, path)

def collect_file(parent, path):
    test_case = os.getenv("APPINSPECT_TEST")
    if test_case is None or path.basename.startswith(test_case):
        return testutils.ScenarioFile(path, parent, packages_dir)
