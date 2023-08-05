# Python Standard Libraries
from __future__ import print_function
import os
import subprocess
import xml.etree.ElementTree as ET
from tempfile import NamedTemporaryFile
import pytest
# Third-Party Libraries
# N/A
# Custom Libraries

def run(cmd):
    """Helper function to run command line calls

    Returns:
        tuple of (Int, String, String): Returns exit_code, stdout and stderr,
            where exit_code is an integer representing the exit code result of
            the command, stdout is the stdout that is created from the command,
            that is run and stderr is the stderror output that is created from
            the command that is run.
    """
    # Use to verify if the command is correct
    process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()
    exit_code = process.returncode
    return exit_code, stdout, stderr


def run_appinspect(args):
    """Helper function to run appinspect on the command line.

    Returns:
        tuple of (Int, String, String): Returns exit_code, stdout and stderr,
            where exit_code is an integer representing the exit code result of
            the command, stdout is the stdout that is created from the command,
            that is run and stderr is the stderror output that is created from
            the command that is run.

    Args:
        args (List of strings): A list of strings to be used for the run command
    """
    appinspect_path = os.path.join('splunk-appinspect')
    command_to_run = [appinspect_path] + args
    print("Performing command: {}".format(" ".join(command_to_run)))
    return run(command_to_run)


def run_appinspect_inspect(args):
    """Helper function to run 'appinspect inspect' command line.

    Returns:
        tuple of (Int, String, String): Returns exit_code, stdout and stderr,
            where exit_code is an integer representing the exit code result of
            the command, stdout is the stdout that is created from the command,
            that is run and stderr is the stderror output that is created from
            the command that is run.

    Args:
        args (List of strings): A list of strings to be used for the run command
    """
    return run_appinspect(['inspect'] + args)


def run_appinspect_list(args):
    """Helper function to run 'appinspect list' command line.

    Returns:
        tuple of (Int, String, String): Returns exit_code, stdout and stderr,
            where exit_code is an integer representing the exit code result of
            the command, stdout is the stdout that is created from the command,
            that is run and stderr is the stderror output that is created from
            the command that is run.

    Args:
        args (List of strings): A list of strings to be used for the run command
    """
    exit_code, stdout, stderr = run_appinspect(['list'] + args)
    return exit_code, stdout, stderr


def run_appinspect_inspect_report_junitxml(output_file, args):
    """Helper function to run appinspect to output junitxml.

    Executes the command
    'appinspect inspect --data-format junitxml --output-file <output_file>'

    Args:
        output_file (String): A path to where the file should be output to
        args (List of strings): A list of strings to be used for the run command

    Returns:
        tuple of (Int, String, String): Returns exit_code, stdout and stderr,
            where exit_code is an integer representing the exit code result of
            the command, stdout is the stdout that is created from the command,
            that is run and stderr is the stderror output that is created from
            the command that is run.

    """
    # TODO: make use of pytest capfd to capture output.
    exit_code, stdout, stderr = run_appinspect_inspect(['--data-format', 'junitxml', '--output-file', output_file] + args)
    assert exit_code == 0
    assert len(stdout) != 0, "stdout was zero bytes."
    assert len(stderr) == 0, "stderr was not zero bytes."
    return exit_code, stdout, stderr


def run_appinspect_inspect_report_json(output_file, args):
    """Helper function to run appinspect to output json.

    Executes the command
    'appinspect inspect --data-format json --output-file <output_file>'

    Args:
        output_file (String): A path to where the file should be output to
        args (List of strings): A list of strings to be used for the run command

    Returns:
        tuple of (Int, String, String): Returns exit_code, stdout and stderr,
            where exit_code is an integer representing the exit code result of
            the command, stdout is the stdout that is created from the command,
            that is run and stderr is the stderror output that is created from
            the command that is run.

    """
    # TODO: make use of pytest capfd to capture output.
    return run_appinspect_inspect(['--data-format', 'json', '--output-file',
                                   output_file] + args)


def find_junitxml_testcase_results(junitxml_results_file, testcase, tag):
    """Helper function to test AppInspect's junitxml results.

    Args:
        junitxml_results_file (String): A path to where the file should be
            output to
        testcase (String): A string representing the check that should have been
            performed during the AppInspect runtime
        tag (String): A string representing the expected result of the check


    Returns:
        List of Element objects: This returns a list of element objects that
            match that tag and testcase passed in
    """
    test_results_tree = ET.parse(junitxml_results_file)
    test_results_tree_root = test_results_tree.getroot()
    return test_results_tree_root.findall(".//{}/..[@name='{}']".format(tag, testcase))


def print_verification_header(instructions):
    print(" " * 80)
    print(" " * 80)
    print("Release Acceptance Test")
    print(" " * 80)
    print("Instructions: ")
    print(instructions)
    print(" " * 80)
    print("See details at https://confluence.splunk.com/display/PROD/AppInspect+CLI+Release+Acceptance+Testing+Instructions")
    print(" " * 80)
    print(" " * 80)
    print("START VERIFY HUMAN READABLE OUTPUT" + " " * 44)
    print("#" * 80)
    print(" " * 80)


def print_verification_footer():
    print(" " * 80)
    print("#" * 80)
    print("END HUMAN READABLE OUTPUT" + " " * 44)
    print("#" * 80)
    print(" " * 80)
    