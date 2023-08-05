"""test_cli_manual_output.py tests splunk-appinspect command-line interface.

This test module is used to validate the run-time of the AppInspect command line
interface (CLI). This is done using a Splunk internal package called Mule, that
can be found here:
https://git.splunk.com/projects/QA/repos/mule/browse

Mule will pull down packages from an Amazon S3 bucket so that we do not have to
inflate the git repository with large packages.

To read more about the S3 bucket being used please see this documentation here:
https://confluence.splunk.com/display/PROD/Test+data+in+Amazon+S3

"""
# Python Standard Libraries
from __future__ import print_function
import os
from tempfile import NamedTemporaryFile
# Third-Party Libraries
# N/A
# Custom Libraries
import test.cli as CLI


APPINSPECT_TEST_CLI_PATH = os.path.dirname(os.path.abspath(__file__))
ROOT_APPINSPECT_TEST_PATH = os.path.abspath(os.path.join(APPINSPECT_TEST_CLI_PATH, os.pardir))
APPINSPECT_TEST_CLI_DATA_BASE_PATH = os.path.join(APPINSPECT_TEST_CLI_PATH, 'packages')

try:
    if not os.environ.get("APPINSPECT_DOWNLOAD_TEST_DATA", "True").lower() == 'false':
        import mule
        PACKAGES_PATH = mule.get("appcert-qa/packages", APPINSPECT_TEST_CLI_PATH)
except:
    pass


def test_splunk_appinspect_human_readable_for_list_version(capsys):
    """Tests that appinspect reports the version and prints for tests.
    See ACD-1835
    """
    instructions = "Please verify the output of the list version command."

    with capsys.disabled():

        CLI.print_verification_header(instructions)
        exit_code, stdout, stderr = CLI.run_appinspect_list(["version"])
        assert exit_code == 0

        # Print the output to view in Jenkins
        print(stdout)
        CLI.print_verification_footer()

def test_splunk_appinspect_human_readable_for_list_checks(capsys):
    """Tests that appinspect reports the list of checks and outputs for manual verification.
    """
    with capsys.disabled():
        instructions = "Please verify the output of the list checks command."
        CLI.print_verification_header(instructions)

        args = ['checks']
        exit_code, stdout, stderr = CLI.run_appinspect_list(args)
        assert exit_code == 0

        # Print the output to view in Jenkins
        print(stdout)
        CLI.print_verification_footer()


def test_splunk_appinspect_inspect_human_readable_for_app_package(capsys):
    """Tests that appinspect inspects the package and outputs for manual verification.
    See ACD-1836
    """
    with capsys.disabled():
        instructions = "Please verify the output of the inspect command on an app."
        CLI.print_verification_header(instructions)
        args = [os.path.join(APPINSPECT_TEST_CLI_DATA_BASE_PATH,
                             'An_App.tgz')]
        temp_file = NamedTemporaryFile(delete=False)  # Don't delete temp file for Windows compatibility
        try:
                exit_code, stdout, stderr = CLI.run_appinspect_inspect(args)
                assert exit_code == 0

                # Print the output to view in Jenkins
                print(stdout)
                CLI.print_verification_footer()

        finally:
            temp_file.close()
            os.remove(temp_file.name)



def test_splunk_appinspect_inspect_human_readable_for_app_package_precert(capsys):
    """Tests that appinspect inspects the package and outputs for manual
    verification in precert mode. See ACD-1838
    """

    with capsys.disabled():
        instructions = "Please verify the output of the inspect command using precert mode on an app."
        CLI.print_verification_header(instructions)
        args = ['--mode', 'precert',
                os.path.join(APPINSPECT_TEST_CLI_DATA_BASE_PATH,'An_App.tgz')]
        temp_file = NamedTemporaryFile(delete=False)  # Don't delete temp file for Windows compatibility
        try:
                exit_code, stdout, stderr = CLI.run_appinspect_inspect(args)
                assert exit_code == 0

                # Print the output to view in Jenkins
                print(stdout)
                CLI.print_verification_footer()

        finally:
            temp_file.close()
            os.remove(temp_file.name)
