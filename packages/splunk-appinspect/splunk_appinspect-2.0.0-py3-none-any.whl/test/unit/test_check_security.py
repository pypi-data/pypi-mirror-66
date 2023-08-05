# Copyright 2018 Splunk Inc. All rights reserved.

import os
import pytest
import imp


def module_path(file_name):
    PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
    return os.path.join(PROJECT_DIR, "splunk_appinspect", "checks", file_name)


@pytest.fixture
def check_security():
    return imp.load_source("check_security", module_path("check_security.py"))


@pytest.mark.parametrize("message, ret", [('password = "not_set"', True),
                                          ("Password = \\'Password", True),
                                          ("token = <YourSecretPassword>", True),
                                          ("token = xxxxxxxx", True),
                                          ("p1=p1 self.Password = xxxxxxxx", True),
                                          ("password = !my233pwd", False),
                                          ("password = '<pwd>>", False),
                                          ("token = '00xx000xxx'", False),
                                          ("password ='value000", False),
                                          ("password = !sdfs=xxxxx", False)])
def test_secret_disclosure_values_whitelist(message, ret, check_security):
    """
    Test the whitelist of secret values
    """
    assert check_security._secret_disclosure_values_whitelist(message) == ret


def test_secret_disclosure_commands_whitelist(check_security):
    """
    Test the commands whitelist of secret messages in props.conf and transforms.conf
    """
    props_file_path = os.path.join('default', 'props.conf')
    transforms_file_path = os.path.join('default', 'transforms.conf')
    invalid_file_path = os.path.join('default', 'inputs.conf')

    # the structure of test_lists is [(file_path, messages, expect_return)]
    test_lists = [(props_file_path, ["SEDCMD-password=mypwd"], True),
                  (props_file_path, ["EXTRACT-password=mypwd"], True),
                  (props_file_path, ["LOOKUP_password = mypwd"], True),
                  (transforms_file_path, ["REGEX = password=123"], True),
                  (transforms_file_path, ["FORMAT=password=$0:$1"], True),
                  (invalid_file_path, ["REGEX=password=123"], False)]

    for test in test_lists:
        assert check_security._secret_disclosure_commands_whitelist(test[0], test[1]) == test[2]
