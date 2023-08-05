"""This module encapsulates the Linux installation tests of the Splunk
AppInspect CLI.

With the exception of the tests mentioning otherwise, all tests are performed
with the assumption that the environment is a clean environment that is provided
before testing.

usage: `pytest test/installation/test_installation_linux.py`
"""

# Copyright 2017 Splunk Inc. All rights reserved.

# Python Standard Libraries
from __future__ import print_function
import logging
import os
import subprocess
# Third-Party Libraries
import pytest
import virtualenv
# Custom Libraries
from . import splunk_appinspect_builds
from .test_installation import TestInstallationBase

logger = logging.getLogger(__name__)

current_directory = os.path.dirname(os.path.abspath(__file__))
repository_root_directory = os.path.abspath(os.path.join(current_directory, "..", ".."))
test_app_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "installation_test_app.tgz")


def print_header(header_title):
    """Helper function to help delineate steps during installation logic

    Returns:
        None
    """
    print("// " + "=" * 77)
    print("// {}".format(header_title))
    print("// " + "=" * 77)


def can_module_be_imported(module_name):
    """Helper function to test module/library installation.

    Arguments:
        module_name (String): the module to install

    Returns:
        Boolean: True if module/library worked, False if it did not
    """
    was_module_imported = False
    try:
        import module_name
        was_module_imported = True
    except ImportError as exception:
        # Do nothing on purpose
        pass

    return was_module_imported


@pytest.mark.skipif(os.name != "posix", reason="Only runs on Linux or OSX platform.")
class TestInstallationOnPosix(TestInstallationBase):
    """Tests installation, upgrading, and uninstallation of splunk-appinspect on
    posix derived systems (OSX, Unix, Linux).
    """

    def setup_method(self, method):
        """General setup method for required resources."""
        self.splunk_appinspect_builds = splunk_appinspect_builds.SplunkAppInspectBuilds()
        self.create_temp_directory()  # for virtualenv in each test if needed

    def teardown_method(self, splunk_appinspect_builds_fixture):
        """General teardown method for required resources."""
        self.splunk_appinspect_builds.teardown_method()
        self.clean_up_temp_directory()

    @staticmethod
    def _verify_installation(env):
        """Helper function to simplify logic for checking if a splunk-appinspect
        artifact is installed and is performing baseline functionality reliably.

        Arguments:
            env (Dictionary of String:String): A dictionary of key value pairs
                that are environment variables to provide for the execution
                of system commands

        Returns:
            None
        """
        try:
            return_value = subprocess.check_call(["which", "splunk-appinspect"], env=env)
            assert return_value == 0, "Command `which splunk-appinspect` failed!"
            return_value = subprocess.check_call(["splunk-appinspect"], env=env)
            assert return_value == 0, "Command `splunk-appinspect` failed!"
            return_value = subprocess.check_call(["splunk-appinspect", "list", "version"], env=env)
            assert return_value == 0, "`Command `splunk-appinspect list version` failed!"
            return_value = subprocess.check_call(["splunk-appinspect", "inspect", test_app_path], env=env)
            assert return_value == 0, "`Command `splunk-appinspect inspect {}` failed!".format(test_app_path)
        except OSError as exception:
            raise Exception("Not installed in fresh virtualenv!", exception)

    def test_installation_using_pip_in_fresh_virtual_env(self):
        """A test to determine that splunk-appinspect can be installed using
        pip as the installation tool in a clean environment.

        The environment is expected to:
        - have virtualenv be responsible for the environment settings
        - be a clean environment
            - global scope is clean
            - local scope is clean
        - be without any previous versions of splunk-appinspect
        - be without any required libraries already installed
        """
        virtualenv.create_environment(self.temporary_directory, clear=True)
        env = os.environ.copy()
        env["PATH"] = self.temporary_directory + "/bin:" + env["PATH"]  # use virtualenv's path

        splunk_appinspect_version_to_install = "latest"
        splunk_appinspect_latest_file_path = self.splunk_appinspect_builds.retrieve_splunk_appinspect_path(splunk_appinspect_version_to_install,
                                                                                                           env=env)

        virtual_pip = self.temporary_directory + "/bin/pip"
        splunk_appinspect_pip_install_latest_command_arguments = [virtual_pip, "install", splunk_appinspect_latest_file_path]
        is_splunk_appinspect_already_installed = can_module_be_imported("splunk-appinspect")
        if is_splunk_appinspect_already_installed:
            print_header("Uninstalling AppInspect")
            subprocess.check_call([virtual_pip, "uninstall", "-y", "splunk-appinspect"],
                                  env=env)

        print_header("Installing AppInspect version {}".format(splunk_appinspect_version_to_install))
        return_value = subprocess.check_call(splunk_appinspect_pip_install_latest_command_arguments,
                                             env=env)

        installation_latest_error_message = ("`test_installation_using_pip_in_fresh_virtual_env` "
                                             " tried to use the command `{}` in order"
                                             " to install splunk-appinspect and failed"
                                             "!").format(" ".join(splunk_appinspect_pip_install_latest_command_arguments))
        assert return_value == 0, installation_latest_error_message

        print_header("Listing Dependencies")
        try:
            subprocess.check_call([virtual_pip, "freeze"],
                                  env=env)
        except Exception as exception:
            print(exception)

        self._verify_installation(env=env)

        subprocess.check_call([virtual_pip, "uninstall", "-y", "splunk-appinspect"],
                              env=env)

    def test_installation_using_pip_over_old_installation_with_virtual_env(self):
        """A test to determine that splunk-appinspect can be installed using
        pip as the installation tool in a dirty environment.

        The environment is expected to:
        - have virtualenv be responsible for the environment settings
        - be a dirty environment
            - global scope may be dirty
            - local scope is dirty
        - have an existing version of splunk-appinspect already installed
        - have existing required libraries already installed
            - can potentially be a different version
        """
        virtualenv.create_environment(self.temporary_directory, clear=True)
        env = os.environ.copy()
        env["PATH"] = self.temporary_directory + "/bin:" + env["PATH"]  # use virtualenv"s path

        splunk_appinspect_1_5_0_string = "1.5.0"
        splunk_appinspect_latest_string = "latest"

        splunk_appinspect_1_5_0_file_path = self.splunk_appinspect_builds.retrieve_splunk_appinspect_path(splunk_appinspect_1_5_0_string,
                                                                                                          env=env)
        splunk_appinspect_latest_file_path = self.splunk_appinspect_builds.retrieve_splunk_appinspect_path(splunk_appinspect_latest_string,
                                                                                                           env=env)

        virtual_pip = self.temporary_directory + "/bin/pip"
        splunk_appinspect_pip_install_1_5_0_command_arguments = [virtual_pip, "install",
                                                                 splunk_appinspect_1_5_0_file_path]
        splunk_appinspect_pip_install_latest_command_arguments = [virtual_pip, "install",
                                                                  splunk_appinspect_latest_file_path]

        is_splunk_appinspect_already_installed = can_module_be_imported("splunk-appinspect")
        if is_splunk_appinspect_already_installed:
            print_header("Uninstalling AppInspect")
            subprocess.check_call([virtual_pip, "uninstall", "-y", "splunk-appinspect"],
                                  env=env)

        print_header("Installing AppInspect version {}".format(splunk_appinspect_1_5_0_string))
        return_value = subprocess.check_call(splunk_appinspect_pip_install_1_5_0_command_arguments,
                                             env=env)
        installation_1_5_0_error_message = ("`test_installation_using_pip_over_old_installation_with_virtual_env` "
                                            " tried to use the command `{}` in order"
                                            " to install splunk-appinspect and failed"
                                            "!").format(" ".join(splunk_appinspect_pip_install_1_5_0_command_arguments))
        assert return_value == 0, installation_1_5_0_error_message

        print_header("Installing AppInspect version latest ({})".format(splunk_appinspect_latest_string))
        return_value = subprocess.check_call(splunk_appinspect_pip_install_latest_command_arguments,
                                             env=env)
        installation_latest_error_message = ("`test_installation_using_pip_over_old_installation_with_virtual_env` "
                                             " tried to use the command `{}` in order"
                                             " to install splunk-appinspect and failed"
                                             "!").format(" ".join(splunk_appinspect_pip_install_latest_command_arguments))
        assert return_value == 0, installation_latest_error_message

        print_header("Listing Dependencies")
        try:
            subprocess.check_call([virtual_pip, "freeze"],
                                  env=env)
        except Exception as exception:
            print(exception)

        self._verify_installation(env=env)

        subprocess.check_call([virtual_pip, "uninstall", "-y", "splunk-appinspect"],
                              env=env)

    def test_installation_using_pip_without_virtual_env(self):
        """A test to determine that splunk-appinspect can be installed using
        pip as the installation tool in the global environment.

        The environment is expected to:
        - potentially be a dirty environment
            - global scope may be dirty
        - have existing required libraries already installed
            - can potentially be a different version
        """
        env = os.environ.copy()

        splunk_appinspect_version_to_install = "latest"
        splunk_appinspect_latest_file_path = self.splunk_appinspect_builds.retrieve_splunk_appinspect_path(splunk_appinspect_version_to_install,
                                                                                                           env=env)

        is_splunk_appinspect_already_installed = can_module_be_imported("splunk-appinspect")
        if is_splunk_appinspect_already_installed:
            print_header("Uninstalling AppInspect")
            subprocess.check_call(["pip", "uninstall", "-y", "splunk-appinspect"])

        print_header("Installing AppInspect version {}".format(splunk_appinspect_version_to_install))
        subprocess.check_call(["pip", "install", splunk_appinspect_latest_file_path])

        print_header("Listing Dependencies")
        try:
            subprocess.check_call(["pip", "freeze"],
                                  env=env)
        except Exception as exception:
            print(exception)

        self._verify_installation(env)

        subprocess.check_call(["pip", "uninstall", "-y", "splunk-appinspect"])

    def test_installation_using_pip_over_old_installation_without_virtual_env(self):
        """A test to determine that splunk-appinspect can be installed using
        pip as the installation tool in the global environment.

        The environment is expected to:
        - be a dirty environment
            - global scope is dirty
        - have an existing version of splunk-appinspect already installed
        - have existing required libraries already installed
            - can potentially be a different version
        """
        env = os.environ.copy()

        splunk_appinspect_1_5_0_string = "1.5.0"
        splunk_appinspect_latest_string = "latest"

        splunk_appinspect_1_5_0_file_path = self.splunk_appinspect_builds.retrieve_splunk_appinspect_path(splunk_appinspect_1_5_0_string,
                                                                                                          env=env)
        splunk_appinspect_latest_file_path = self.splunk_appinspect_builds.retrieve_splunk_appinspect_path(splunk_appinspect_latest_string,
                                                                                                           env=env)

        is_splunk_appinspect_already_installed = can_module_be_imported("splunk-appinspect")
        if is_splunk_appinspect_already_installed:
            print_header("Uninstalling AppInspect")
            subprocess.check_call(["pip", "uninstall", "-y", "splunk-appinspect"])

        print_header("Installing AppInspect version {}".format(splunk_appinspect_1_5_0_string))
        subprocess.check_call(["pip", "install", splunk_appinspect_1_5_0_file_path])

        print_header("Installing AppInspect version latest ({})".format(splunk_appinspect_latest_string))
        subprocess.check_call(["pip", "install", splunk_appinspect_latest_file_path])

        print_header("Listing Dependencies")
        try:
            subprocess.check_call(["pip", "freeze"])
        except Exception as exception:
            print(exception)

        self._verify_installation(env)

        subprocess.check_call(["pip", "uninstall", "-y", "splunk-appinspect"])
