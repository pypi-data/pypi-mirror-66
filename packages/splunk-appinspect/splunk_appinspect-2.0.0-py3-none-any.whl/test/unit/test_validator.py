"""Copyright 2017 Splunk Inc. All rights reserved."""

# Python Standard Libraries
import os
# Third-Party Library
# Custom Libraries
import splunk_appinspect
from splunk_appinspect.validator import Validator
from splunk_appinspect.app_package_handler import AppPackageHandler
from splunk_appinspect.listeners.listener import Listener

APP_PACKAGES = os.path.join(os.path.abspath(os.path.dirname(
    __file__)), 'packages', 'app_package_testing_packages')
PACKAGES = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'packages')
GOOD_TGZ = os.path.join(APP_PACKAGES, 'good_app_conf.tgz')
IS_HIDDEN_TAR_GZ = os.path.join(APP_PACKAGES, '.is_a_hidden_tar_gz_package-ACD-1362.tar.gz')
MISSING_APP_CONF_SPL = os.path.join(APP_PACKAGES, 'has_missing_app_conf_file-ACD-1362.spl')
HAS_HIDDEN_DEPENDENCIES_DIRECTORY = os.path.join(APP_PACKAGES, 'has_hidden_dependencies_directory-ACD-1556.spl')


class MockListener(Listener):
    """A test listener"""

    def __init__(self):
        """Basic init"""
        self.event_list = {}

    def __add_event(self, event):
        if event in self.event_list.keys():
            self.event_list[event] = self.event_list[event] + 1
        else:
            self.event_list[event] = 1

    def on_start_validation(self, app_names):
        """Mock event"""
        self.__add_event("start_validation")

    def on_start_app(self, app):
        """Mock event"""
        self.__add_event("start_app")

    def on_start_package_validation(self, app_names):
        """Mock event"""
        self.__add_event("start_package_validation")

    def on_finish_package_validation(self, app_names):
        """Mock event"""
        self.__add_event("finish_package_validation")

    def on_start_app_validation(self, app_names):
        """Mock event"""
        self.__add_event("start_app_validation")

    def on_finish_app_validation(self, app_names):
        """Mock event"""
        self.__add_event("finish_app_validation")

    def on_start_dispatching_group(self, group, checks):
        """Mock event"""
        self.__add_event("start_dispatching_group")

    def on_start_check(self, check):
        """Mock event"""
        self.__add_event("start_check")

    def on_finish_check(self, check, result):
        """Mock event"""
        self.__add_event("finish_check")

    def on_finish_dispatching_group(self, group, checks):
        """Mock event"""
        self.__add_event("finish_dispatching_group")

    def on_finish_app(self, app, result):
        """Mock event"""
        self.__add_event("finish_app")

    def on_finish_validation(self, app_names, validation_report):
        """Mock event"""
        self.__add_event("finish_validation")
    
    def on_enable_python_analyzer(self):
        """Mock event"""
        self.__add_event("enable_python_analyzer")

    def event_count(self, event):
        """Returns the count of events"""
        if event in self.event_list.keys():
            return self.event_list[event]
        else:
            return 0


def test_validator_init_with_basic_package():
    """Test setup of the Validator."""
    handler = AppPackageHandler(GOOD_TGZ)
    validator = Validator(handler)
    assert validator


def test_validator_validate_with_basic_package():
    """Test setup of the Validator."""
    handler = AppPackageHandler(GOOD_TGZ)
    validator = Validator(handler)
    validator.validate()
    assert not validator.validation_report.has_invalid_packages


def test_validator_validate_emits_events_good_app():
    """Test events are emitted."""
    handler = AppPackageHandler(GOOD_TGZ)
    test_listener = MockListener()
    grps = splunk_appinspect.checks.groups()
    validator = Validator(handler, groups_to_validate=grps, listeners=[test_listener])
    validator.validate()

    assert test_listener.event_count("start_validation") == 1
    assert test_listener.event_count("start_app") == 1
    assert test_listener.event_count("start_package_validation") == 1
    assert test_listener.event_count("finish_package_validation") == 1
    assert test_listener.event_count("start_app_validation") == 1
    assert test_listener.event_count("start_dispatching_group") >= 1
    assert test_listener.event_count("start_check") >= 1
    assert test_listener.event_count("finish_check") >= 1
    assert test_listener.event_count("finish_dispatching_group") >= 1
    assert test_listener.event_count("finish_app_validation") == 1
    assert test_listener.event_count("finish_app") == 1
    assert test_listener.event_count("finish_validation") == 1
    assert test_listener.event_count("enable_python_analyzer") == 1


def test_validator_validate_emits_events_malformed_app():
    """Test events are emitted."""
    handler = AppPackageHandler(MISSING_APP_CONF_SPL)
    test_listener = MockListener()
    validator = Validator(handler, listeners=[test_listener])
    validator.validate()

    assert test_listener.event_count("start_validation") == 1
    assert test_listener.event_count("start_app") == 1
    assert test_listener.event_count("start_package_validation") == 1
    assert test_listener.event_count("finish_package_validation") == 1
    assert test_listener.event_count("start_app_validation") == 0
    assert test_listener.event_count("start_dispatching_group") >= 1
    assert test_listener.event_count("start_check") >= 1
    assert test_listener.event_count("finish_check") >= 1
    assert test_listener.event_count("finish_dispatching_group") >= 1
    assert test_listener.event_count("finish_app_validation") == 0
    assert test_listener.event_count("finish_app") == 1
    assert test_listener.event_count("finish_validation") == 1


def test_validator_validate_emits_events_malformed_app_with_groups():
    """Test events are emitted."""
    handler = AppPackageHandler(MISSING_APP_CONF_SPL)
    test_listener = MockListener()
    grps = splunk_appinspect.checks.groups()
    validator = Validator(handler, groups_to_validate=grps, listeners=[test_listener])
    validator.validate()

    assert test_listener.event_count("start_validation") == 1
    assert test_listener.event_count("start_app") == 1
    assert test_listener.event_count("start_package_validation") == 1
    assert test_listener.event_count("finish_package_validation") == 1
    # Validation events should not be raised as packaging has issues
    assert test_listener.event_count("start_app_validation") == 0
    assert test_listener.event_count("start_dispatching_group") >= 1
    assert test_listener.event_count("start_check") >= 1
    assert test_listener.event_count("finish_check") >= 1
    assert test_listener.event_count("finish_dispatching_group") >= 1
    # Validation events should not be raised as packaging has issues
    assert test_listener.event_count("finish_app_validation") == 0
    assert test_listener.event_count("finish_app") == 1
    assert test_listener.event_count("finish_validation") == 1


def test_validator_validate_returns_report_with_validation_issues():
    """Test events are emitted."""
    handler = AppPackageHandler(MISSING_APP_CONF_SPL)
    test_listener = MockListener()
    grps = splunk_appinspect.checks.groups()
    validator = Validator(handler, groups_to_validate=grps, listeners=[test_listener])
    validator.validate()
    assert validator.validation_report.has_invalid_packages


def test_validator_validate_returns_report_for_app_with_hidden_dependencies():
    """Test events are emitted."""
    handler = AppPackageHandler(HAS_HIDDEN_DEPENDENCIES_DIRECTORY)
    test_listener = MockListener()
    grps = splunk_appinspect.checks.groups()
    validator = Validator(handler, groups_to_validate=grps, listeners=[test_listener])
    validator.validate()
    assert not validator.validation_report.has_invalid_packages


def test_validator_validate_with_python_analyzer_disabled():
    """Test events are emitted."""
    handler = AppPackageHandler(GOOD_TGZ)
    test_listener = MockListener()
    grps = splunk_appinspect.checks.groups(included_tags=['cloud'], excluded_tags=['ast'])
    validator = Validator(handler,
                          groups_to_validate=grps,
                          listeners=[test_listener])
    validator.validate()

    assert test_listener.event_count("enable_python_analyzer") == 0