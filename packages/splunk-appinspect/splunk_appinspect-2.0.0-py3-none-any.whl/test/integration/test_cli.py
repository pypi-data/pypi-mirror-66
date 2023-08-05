"""test_cli.py tests splunk-appinspect command-line interface.

This test module is used to validate the run-time of the AppInspect command line
interface (CLI). This is done using a Splunk internal package called Mule, that
can be found here:
https://git.splunk.com/projects/QA/repos/mule/browse

Mule will pull down packages from an Amazon S3 bucket so that we do not have to
inflate the git repository with large packages.

To read more about the S3 bucket being used please see this documentation here:
https://confluence.splunk.com/display/PROD/Test+data+in+Amazon+S3

usage: 'pytest test_cli.py'
"""
# Python Standard Libraries
from __future__ import print_function
import os
import xml.etree.ElementTree as ET
import pytest
import shutil
import tarfile
import tempfile
# Third-Party Libraries
# N/A
# Custom Libraries
from .. import cli as CLI


APPINSPECT_TEST_CLI_PATH = os.path.dirname(os.path.abspath(__file__))
ROOT_APPINSPECT_TEST_PATH = os.path.abspath(os.path.join(APPINSPECT_TEST_CLI_PATH, os.pardir))
APPINSPECT_TEST_CLI_DATA_BASE_PATH = os.path.join(APPINSPECT_TEST_CLI_PATH, 'packages')

try:
    if not os.environ.get("APPINSPECT_DOWNLOAD_TEST_DATA", "True").lower() == 'false':
        import mule
        PACKAGES_PATH = mule.get("appcert-qa/packages", APPINSPECT_TEST_CLI_PATH)
except:
    pass


# ------------------------------------------------------------------------------
# Test `splunk-appinspect` installation
# ------------------------------------------------------------------------------
def test_splunk_appinspect_is_installed():
    """Test to make sure splunk-appinspect CLI has been installed."""

    # TODO: walk the search path to find cli
    # assert os.path.isfile(appinspect_cli) == True
    try:
        import splunk_appinspect
        del splunk_appinspect
    except ImportError:
        assert False


# ------------------------------------------------------------------------------
# Test `splunk-appinspect list` command
# ------------------------------------------------------------------------------
def test_splunk_appinspect_list_checks_pass():
    """Tests that the command 'splunk-appinspect list checks' works."""

    args = ['checks']
    exit_code, stdout, stderr = CLI.run_appinspect_list(args)
    assert len(stderr) == 0, "stderr was not zero bytes. STDERR: {}".format(stderr)
    assert exit_code == 0, "The exit code was {}".format(exit_code)
    assert len(stdout) != 0, "stdout was zero bytes. STDOUT: {}".format(stdout)


def test_splunk_appinspect_list_groups_pass():
    """Tests that the command 'splunk-appinspect list groups' works."""

    args = ['groups']
    exit_code, stdout, stderr = CLI.run_appinspect_list(args)
    assert len(stderr) == 0, "stderr was not zero bytes. STDERR: {}".format(stderr)
    assert exit_code == 0, "The exit code was {}".format(exit_code)
    assert len(stdout) != 0, "stdout was zero bytes. STDOUT: {}".format(stdout)


def test_splunk_appinspect_list_tags_pass():
    """Tests that the command 'splunk-appinspect list tags' works."""

    args = ['tags']
    exit_code, stdout, stderr = CLI.run_appinspect_list(args)
    assert len(stderr) == 0, "stderr was not zero bytes. STDERR: {}".format(stderr)
    assert exit_code == 0, "The exit code was {}".format(exit_code)
    assert len(stdout) != 0, "stdout was zero bytes. STDOUT: {}".format(stdout)


def test_splunk_appinspect_list_version_pass():
    """Tests that the command 'splunk-appinspect list tags' works."""

    args = ['version']
    exit_code, stdout, stderr = CLI.run_appinspect_list(args)
    assert len(stderr) == 0, "stderr was not zero bytes. STDERR: {}".format(stderr)
    assert exit_code == 0, "The exit code was {}".format(exit_code)
    assert len(stdout) != 0, "stdout was zero bytes. STDOUT: {}".format(stdout)


def test_splunk_appinspect_list_groups_checks_tags_pass():
    """Tests that the command 'splunk-appinspect list groups checks tags'
    works.
    """

    args = ['groups', 'checks', 'tags', 'version']
    exit_code, stdout, stderr = CLI.run_appinspect_list(args)
    assert len(stderr) == 0, "stderr was not zero bytes. STDERR: {}".format(stderr)
    assert exit_code == 0, "The exit code was {}".format(exit_code)
    assert len(stdout) != 0, "stdout was zero bytes. STDOUT: {}".format(stdout)


def test_splunk_appinspect_list_works_with_included_tags_filter():
    """Tests that the command 'splunk-appinspect list' command works using the
    --included-tags filter.
    """

    args = ['checks', '--included-tags', 'manual']
    exit_code, stdout, stderr = CLI.run_appinspect_list(args)
    assert len(stderr) == 0, "stderr was not zero bytes. STDERR: {}".format(stderr)
    assert exit_code == 0, "The exit code was {}".format(exit_code)
    assert len(stdout) != 0, "stdout was zero bytes. STDOUT: {}".format(stdout)


def test_splunk_appinspect_list_works_with_excluded_tags_filter():
    """Tests that the command 'splunk-appinspect list' command works using the
    --excluded-tags filter.
    """

    args = ['checks', '--excluded-tags', 'splunkapps']
    exit_code, stdout, stderr = CLI.run_appinspect_list(args)
    assert len(stderr) == 0, "stderr was not zero bytes. STDERR: {}".format(stderr)
    assert exit_code == 0, "The exit code was {}".format(exit_code)
    assert len(stdout) != 0, "stdout was zero bytes. STDOUT: {}".format(stdout)


def test_splunk_appinspect_list_works_with_included_and_excluded_tags_filter():
    """Tests that the command 'splunk-appinspect list' command works using the
    --included-tags and --excluded-tags filter.
    """

    args = ['checks', '--included-tags', 'cloud', '--excluded-tags', 'manual']
    exit_code, stdout, stderr = CLI.run_appinspect_list(args)
    assert len(stderr) == 0, "stderr was not zero bytes. STDERR: {}".format(stderr)
    assert exit_code == 0, "The exit code was {}".format(exit_code)
    assert len(stdout) != 0, "stdout was zero bytes. STDOUT: {}".format(stdout)

# ------------------------------------------------------------------------------
# Test `splunk-appinspect documentation` command
# ------------------------------------------------------------------------------
# TODO: Refactor specific command validation to separate files


def test_splunk_appinspect_documentation_command_does_not_fail():
    """Test that the `splunk-appinspect documentation` command does not blow up
    when used without inputs.
    """
    args = ['documentation']
    exit_code, stdout, stderr = CLI.run_appinspect_list(args)
    assert len(stderr) == 0, "stderr was not zero bytes. STDERR: {}".format(stderr)
    assert exit_code == 0, "The exit code was {}".format(exit_code)
    assert len(stdout) != 0, "stdout was zero bytes. STDOUT: {}".format(stdout)


def test_splunk_appinspect_documentation_criteria_command_stream_output_does_not_fail():
    """Test that the `splunk-appinspect documentation criteria` command does
    returns output to the command line when no options are provided.
    """
    args = ['documentation', 'criteria']
    exit_code, stdout, stderr = CLI.run_appinspect_list(args)
    assert len(stderr) == 0, "stderr was not zero bytes. STDERR: {}".format(stderr)
    assert exit_code == 0, "The exit code was {}".format(exit_code)
    assert len(stdout) != 0, "stdout was zero bytes. STDOUT: {}".format(stdout)


def test_splunk_appinspect_documentation_criteria_command_file_output_does_not_fail():
    """Test that the `splunk-appinspect documentation criteria` command returns
    output to a specified file when the `--output-file` option is used.
    """
    try:
        temporary_directory_path = tempfile.mkdtemp()
        new_file_path = os.path.join(temporary_directory_path, "output_file.html")

        args = ["documentation", "criteria",
                "--ouput-file", new_file_path]
        exit_code, stdout, stderr = CLI.run_appinspect_list(args)

        assert len(stderr) == 0, "stderr was not zero bytes. STDERR: {}".format(stderr)
        assert exit_code == 0, "The exit code was {}".format(exit_code)
        assert len(stdout) != 0, "stdout was zero bytes. STDOUT: {}".format(stdout)

        assert os.path.isfile(new_file_path)
    except Exception as exception:
        print(exception)
    finally:
        shutil.rmtree(temporary_directory_path)


def test_splunk_appinspect_documentation_criteria_command_using_tags_file_output_does_not_fail():
    """Test that the `splunk-appinspect documentation criteria` command returns
    output to a specified file when the `--output-file` and `--included-tags`
    option is used.
    """
    try:
        temporary_directory_path = tempfile.mkdtemp()
        new_file_path = os.path.join(temporary_directory_path, "output_file.html")

        args = ["documentation", "criteria",
                "--included-tags", "splunk_appinspect",
                "--included-tags", "cloud",
                "--ouput-file", new_file_path]
        exit_code, stdout, stderr = CLI.run_appinspect_list(args)

        assert len(stdout) != 0, "stdout was zero bytes. STDOUT: {}".format(stdout)
        assert len(stderr) == 0, "stderr was not zero bytes. STDERR: {}".format(stderr)
        assert exit_code == 0, "The exit code was {}".format(exit_code)

        assert os.path.isfile(new_file_path)
    except Exception as exception:
        print(exception)
    finally:
        shutil.rmtree(temporary_directory_path)


# ------------------------------------------------------------------------------
# Test `splunk-appinspect inspect` command
# ------------------------------------------------------------------------------
def test_appinspect_inspect_max_message_fail():
    """Negative tests for running 'appinspect inspect' command with max-message
    option (added in ACD-483) works. This covers the cases of empty value, zero,
    negative, or string values that are not 'all'.
    """

    args = ['--max-messages']
    exit_code, stdout, stderr = CLI.run_appinspect_inspect(args)
    assert len(stderr) != 0, "stderr was zero bytes".format(stderr)
    assert exit_code == 2, "The exit code was {}".format(exit_code)
    assert len(stdout) == 0, "stdout was not zero bytes".format(stdout)

    args = ['--max-messages', '0']
    exit_code, stdout, stderr = CLI.run_appinspect_inspect(args)
    assert len(stderr) != 0, "stderr was zero bytes".format(stderr)
    assert exit_code == 2, "The exit code was {}".format(exit_code)
    assert len(stdout) == 0, "stdout was not zero bytes".format(stdout)

    args = ['--max-messages', '-100']
    exit_code, stdout, stderr = CLI.run_appinspect_inspect(args)
    assert len(stderr) != 0, "stderr was zero bytes".format(stderr)
    assert exit_code == 2, "The exit code was {}".format(exit_code)
    assert len(stdout) == 0, "stdout was not zero bytes".format(stdout)

    args = ['--max-messages', 'foobar']
    exit_code, stdout, stderr = CLI.run_appinspect_inspect(args)
    assert len(stderr) != 0, "stderr was zero bytes".format(stderr)
    assert exit_code == 2, "The exit code was {}".format(exit_code)
    assert len(stdout) == 0, "stdout was not zero bytes".format(stdout)


def test_appinspect_inspect_max_message_pass():
    """Sanity test for running 'appinspect inspect' command with max-message
    option (added in ACD-483 and ACD-1317) works.
    output is not being checked here
    """
    args_1 = ['--max-messages', '2',
              os.path.join(APPINSPECT_TEST_CLI_DATA_BASE_PATH,
                           'splunk-app-for-netapp-data-ontap_213.tgz')]
    args_2 = ['--max-messages', '25',
              os.path.join(APPINSPECT_TEST_CLI_DATA_BASE_PATH,
                           'splunk-app-for-netapp-data-ontap_213.tgz')]
    args_3 = ['--max-messages', 'all',
              os.path.join(APPINSPECT_TEST_CLI_DATA_BASE_PATH,
                           'splunk-app-for-netapp-data-ontap_213.tgz')]
    temp_file_1 = tempfile.NamedTemporaryFile(delete=False)  # Don't delete temp file for Windows compatibility
    temp_file_2 = tempfile.NamedTemporaryFile(delete=False)
    temp_file_3 = tempfile.NamedTemporaryFile(delete=False)
    try:
        exit_code, stdout, stderr = CLI.run_appinspect_inspect_report_json(temp_file_1.name, args_1)
        assert len(stderr) == 0, "stderr was not zero bytes. STDERR: {}".format(stderr)
        assert exit_code == 0, "The exit code was {}".format(exit_code)
        assert len(stdout) != 0, "stdout was zero bytes. STDOUT: {}".format(stdout).format(stdout)

        exit_code, stdout, stderr = CLI.run_appinspect_inspect_report_json(temp_file_2.name, args_2)
        assert len(stderr) == 0, "stderr was not zero bytes. STDERR: {}".format(stderr)
        assert exit_code == 0, "The exit code was {}".format(exit_code)
        assert len(stdout) != 0, "stdout was zero bytes. STDOUT: {}".format(stdout).format(stdout)

        exit_code, stdout, stderr = CLI.run_appinspect_inspect_report_json(temp_file_3.name, args_3)
        assert len(stderr) == 0, "stderr was not zero bytes. STDERR: {}".format(stderr)
        assert exit_code == 0, "The exit code was {}".format(exit_code)
        assert len(stdout) != 0, "stdout was zero bytes. STDOUT: {}".format(stdout).format(stdout)
    finally:
        temp_file_1.close()
        temp_file_2.close()
        temp_file_3.close()
        os.remove(temp_file_1.name)
        os.remove(temp_file_2.name)
        os.remove(temp_file_3.name)


def test_splunk_appinspect_cloud_tag_dashboard_app_pass():
    """Tests that a simple dashboard app can pass the Cloud checks."""

    args = ['--included-tags', 'cloud',
            os.path.join(APPINSPECT_TEST_CLI_DATA_BASE_PATH,
                         'add-on-for-microsoft-forefront-threat-management-gateway_102.tgz')]
    temp_file = tempfile.NamedTemporaryFile(delete=False)  # Don't delete temp file for Windows compatibility
    try:
        exit_code, stdout, stderr = CLI.run_appinspect_inspect_report_junitxml(temp_file.name, args)
    finally:
        temp_file.close()
        os.remove(temp_file.name)


def test_splunk_appinspect_dashboard_app_fail():
    """Tests that a simple dashboard app fails 1 check."""
    args = [os.path.join(APPINSPECT_TEST_CLI_DATA_BASE_PATH,
                         'add-on-for-microsoft-forefront-threat-management-gateway_102.tgz')]
    temp_file = tempfile.NamedTemporaryFile(delete=False)  # Don't delete temp file for Windows compatibility
    try:
        exit_code, stdout, stderr = CLI.run_appinspect_inspect_report_junitxml(temp_file.name, args)
        # Verify that the 'check_that_setup_has_not_been_performed' failed
        assert CLI.find_junitxml_testcase_results(temp_file.name,
                                                  'check_that_setup_has_not_been_performed',
                                                  'failure')
        # Verify that the 'check_transforms_conf_for_external_cmd' passed
        assert not CLI.find_junitxml_testcase_results(temp_file.name,
                                                      'check_transforms_conf_for_external_cmd',
                                                      'failure')  # find "system-out" to make this test fail.
    finally:
        temp_file.close()
        os.remove(temp_file.name)


def test_splunk_appinspect_mode_precert_dashboard_app_fail():
    """Tests that the command '--mode precert' works using a simple dashboard
    app.
    """
    args = ['--mode', 'precert',
            os.path.join(
                APPINSPECT_TEST_CLI_DATA_BASE_PATH,
                'add-on-for-microsoft-forefront-threat-management-gateway_102.tgz'
            )]
    temp_file = tempfile.NamedTemporaryFile(delete=False)  # Don't delete temp file for Windows compatibility
    try:
        exit_code, stdout, stderr = CLI.run_appinspect_inspect_report_junitxml(temp_file.name, args)
        # Verify that the 'check_that_setup_has_not_been_performed' failed
        assert CLI.find_junitxml_testcase_results(temp_file.name,
                                                  'check_that_setup_has_not_been_performed',
                                                  'failure')
        # Verify that the 'check_transforms_conf_for_external_cmd' passed
        assert not CLI.find_junitxml_testcase_results(temp_file.name,
                                                      'check_transforms_conf_for_external_cmd',
                                                      'failure')  # find "system-out" to make this test fail.
    finally:
        temp_file.close()
        os.remove(temp_file.name)


def test_splunk_appinspect_huge_app_fail():
    """Tests appinspect executes on an that contains 1500 files and 500k lines
    of code. This test expects failures for checks. Tests for performance
    regresssions and memory usage.
    """
    args = [os.path.join(APPINSPECT_TEST_CLI_DATA_BASE_PATH, 'splunk-app-for-aws_420.tgz')]
    temp_file = tempfile.NamedTemporaryFile(delete=False)  # Don't delete temp file for Windows compatibility
    try:
        exit_code, stdout, stderr = CLI.run_appinspect_inspect_report_junitxml(temp_file.name, args)
        # this app has several issues, but the exact number of failed checks,
        # isn't as important as being able process this beast without crashing.
    finally:
        temp_file.close()
        os.remove(temp_file.name)


def test_splunk_appinspect_malformed_missing_app_conf():
    """Tests the AppInspect error code returned when an app that is missing an
    app.conf is supplied (ACD-874).
    """
    test_package_path = os.path.join("test",
                                     "unit",
                                     "packages",
                                     "app_package_testing_packages",
                                     "has_missing_app_conf_file-ACD-1362.spl")
    args = [test_package_path]
    exit_code, stdout, stderr = CLI.run_appinspect_inspect(args)
    assert len(stderr) == 0, "stderr was not zero bytes. STDERR: {}".format(stderr)
    assert exit_code == 3, "The exit code was {}".format(exit_code)
    assert len(stdout) != 0, "stdout was zero bytes. STDOUT: {}".format(stdout).format(stdout)


def test_splunk_appinspect_acd_1103():
    """Tests that appinspect reports error when run on package in ACD-1103,

    ACD-1103 contains miscellaneous files not structured as an app.
    """
    args = [os.path.join(APPINSPECT_TEST_CLI_DATA_BASE_PATH, 'ACD-1103.tgz')]
    exit_code, stdout, stderr = CLI.run_appinspect_inspect(args)
    assert len(stderr) == 0, "stderr was not zero bytes. STDERR: {}".format(stderr)
    assert exit_code != 0, "The exit code was {}".format(exit_code)
    assert len(stdout) != 0, "stdout was zero bytes. STDOUT: {}".format(stdout)


def test_splunk_appinspect_acd_875():
    """Tests that appinspect can run on problem app from ACD-875 without
    blowing up.
    """
    args = [os.path.join(APPINSPECT_TEST_CLI_DATA_BASE_PATH, 'ACD-875.tgz')]
    exit_code, stdout, stderr = CLI.run_appinspect_inspect(args)
    assert len(stderr) == 0, "stderr was not zero bytes. STDERR: {}".format(stderr)
    assert exit_code == 3, "The exit code was {}".format(exit_code)
    assert len(stdout) != 0, "stdout was zero bytes. STDOUT: {}".format(stdout).format(stdout)


def test_splunk_appinspect_app_containing_apps():
    """Tests that appinspect can run on an app containing sub-apps."""
    args = [os.path.join(APPINSPECT_TEST_CLI_DATA_BASE_PATH,
                         'splunk-app-for-netapp-data-ontap_213.tgz')]
    temp_file = tempfile.NamedTemporaryFile(delete=False)  # Don't delete temp file for Windows compatibility
    try:
        exit_code, stdout, stderr = CLI.run_appinspect_inspect_report_junitxml(temp_file.name, args)
    finally:
        temp_file.close()
        os.remove(temp_file.name)


def test_splunk_appinspect_add_on_builder_sample():
    """Tests that appinspect can run on an app containing sub-apps."""
    args = [os.path.join(APPINSPECT_TEST_CLI_DATA_BASE_PATH,
                         'TA-AoB_Sample-2.2.0.spl')]
    temp_file = tempfile.NamedTemporaryFile(delete=False)  # Don't delete temp file for Windows compatibility
    try:
        exit_code, stdout, stderr = CLI.run_appinspect_inspect_report_junitxml(temp_file.name, args)
        test_results_tree = ET.parse(temp_file.name)
        test_results_tree_root = test_results_tree.getroot()
        assert test_results_tree_root.find("testsuite").attrib['failures'] == "0"
        assert test_results_tree_root.find("testsuite").attrib['errors'] == "0"
    finally:
        temp_file.close()
        os.remove(temp_file.name)


hidden_dependencies_directory_packages = [
    (os.path.join(ROOT_APPINSPECT_TEST_PATH, "unit", "packages", "app_package_testing_packages", "has_hidden_dependencies_directory-ACD-1556")),
    (os.path.join(ROOT_APPINSPECT_TEST_PATH, "unit", "packages", "app_package_testing_packages", "has_hidden_dependencies_directory-ACD-1556.spl")),
    (os.path.join(ROOT_APPINSPECT_TEST_PATH, "unit", "packages", "app_package_testing_packages", "has_hidden_dependencies_directory-ACD-1556.tar.gz")),
    (os.path.join(ROOT_APPINSPECT_TEST_PATH, "unit", "packages", "app_package_testing_packages", "has_hidden_dependencies_directory-ACD-1556.tgz")),
    (os.path.join(ROOT_APPINSPECT_TEST_PATH, "unit", "packages", "app_package_testing_packages", "has_hidden_dependencies_directory-ACD-1556.zip")),
]


@pytest.mark.parametrize("test_package_path", hidden_dependencies_directory_packages)
def test_splunk_appinspect_app_containing_containing_dependencies_directory(test_package_path):
    """Tests that AppInspect will execute without failing on a Splunk App with a
    dependencies directory.
    """
    temp_file = tempfile.NamedTemporaryFile(delete=False)  # Don't delete temp file for Windows compatibility
    try:
        exit_code, stdout, stderr = CLI.run_appinspect_inspect([test_package_path])
    finally:
        temp_file.close()
        os.remove(temp_file.name)


def test_splunk_appinspect_aob_2_2_0():
    """Tests the AppInspect error code returned when an app that is missing an
    app.conf is supplied (ACD-874).
    """
    test_package_path = os.path.join("test",
                                     "unit",
                                     "packages",
                                     "app_package_testing_packages",
                                     "ta_aob_sample_2_2_0-1.0.0.spl")
    args = [test_package_path]
    exit_code, stdout, stderr = CLI.run_appinspect_inspect(args)
    assert exit_code == 0, "The exit code was {}".format(exit_code)


def test_splunk_appinspect_raw_directory():
    """Tests that AppInspect will execute without failing for raw directory.
    """
    # extract An_App.tgz
    src_path = os.path.join(APPINSPECT_TEST_CLI_DATA_BASE_PATH, "An_App.tgz")
    t = tarfile.open(src_path, "r:gz")
    t.extractall(path=APPINSPECT_TEST_CLI_DATA_BASE_PATH)
    t.close()

    test_package_path = os.path.join(APPINSPECT_TEST_CLI_DATA_BASE_PATH, "brisbane_ferries")
    args = [test_package_path]
    exit_code, stdout, stderr = CLI.run_appinspect_inspect(args)
    assert len(stderr) == 0, "stderr was not zero bytes. STDERR: {}".format(stderr)
    assert exit_code == 0, "The exit code was {}".format(exit_code)
    assert len(stdout) != 0, "stdout was zero bytes. STDOUT: {}".format(stdout).format(stdout)


def test_splunk_appinspect_handle_apps_with_non_ascii_encoding_conf():
    test_package_path = os.path.join("test",
                                     "unit",
                                     "packages",
                                     "app_package_testing_packages",
                                     "non_ascii_app.spl")
    args = [test_package_path]
    exit_code, stdout, stderr = CLI.run_appinspect_inspect(args)
    print(exit_code, stdout, stderr)
    assert exit_code == 0, "The exit code was {}".format(exit_code)


