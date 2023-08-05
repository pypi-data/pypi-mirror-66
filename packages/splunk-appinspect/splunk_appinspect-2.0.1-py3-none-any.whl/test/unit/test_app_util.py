import os
import pytest

import splunk_appinspect.app_util

@pytest.mark.skipif(os.name != "posix", reason="Only runs on Linux or OSX platform.")
def test_outside_app_for_nix():
    testcases = (
        ('$SPLUNK_HOME/etc/apps/test_app/', False),
        ('$SPLUNK_HOME/etc/apps/test_app/../', True),
        ('$SPLUNK_HOME/etc/apps/aws/', True),
        ('$SPLUNK_HOME/etc/apps/', True),
        ('$SPLUNK_HOME/path/', True),
        ('/path', True),
        ('../path', True),
        ('./path', True),
        ('./', True),
        ('../', True),
        ('<command>', False),  # Not a path
        ('python', False),  # Not a path
        ('python.path', False),  # Not a path
        ('.path', False),  # Not a path
        ('999', False),  # Not a path
    )
    for path, result in testcases:
        assert splunk_appinspect.app_util.is_manipulation_outside_of_app_container(path, 'test_app') == result

@pytest.mark.skipif(os.name == "posix", reason="Only runs on Windows platform.")
def test_outside_app_for_windows():
    testcases = (
        ('%SPLUNK_HOME%\\etc\\apps\\test_app\\', False),
        ('%SPLUNK_HOME%\\etc\\apps\\test_app\\..\\', True),
        ('%SPLUNK_HOME%\\etc\\apps\\aws\\', True),
        ('%SPLUNK_HOME%\\etc\\apps\\', True),
        ('%SPLUNK_HOME%\\path\\', True),
        ('$SPLUNK_HOME\\etc\\apps\\test_app\\', False),
        ('$SPLUNK_HOME\\etc\\apps\\test_app\\..\\', True),
        ('$SPLUNK_HOME\\etc\\apps\\aws\\', True),
        ('$SPLUNK_HOME\\etc\\apps\\', True),
        ('$SPLUNK_HOME\\path\\', True),
        ('C:\\path1\\path2\\', True),
        ('\\path', True),
        ('..\\path', True),
        ('.\\path', True),
        ('.\\', True),
        ('..\\', True),
        ('<command>', False),  # Not a path
        ('python', False),  # Not a path
        ('python.path', False),  # Not a path
        ('.path', False),  # Not a path
        ('999', False),  # Not a path
    )
    for path, result in testcases:
        assert splunk_appinspect.app_util.is_manipulation_outside_of_app_container(path, 'test_app') == result