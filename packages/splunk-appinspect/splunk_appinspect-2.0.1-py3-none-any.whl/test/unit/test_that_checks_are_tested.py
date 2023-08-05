# Copyright 2016 Splunk Inc. All rights reserved.

"""This is a test to test that the cert tests have been tested.

It's not just funny to type- it's pretty hard to keep track of which 
certification checks have tests and which don't (yet).
"""

# Python Standard Libraries
import collections
import csv
import logging
import os
import re
# Third-Party Libraries
import pytest
import six
from six import iteritems
# Custom Libraries
import splunk_appinspect

logger = logging.getLogger(__name__)

group_and_check_tuples = []
for group in splunk_appinspect.checks.groups():
    for check in group.checks():
        group_and_check_tuples.append((group.name, check.name))


# A little redundant in that it gets the absolute path, then only uses the
# filename without the 'test_' prefix.
current_directory = os.path.dirname(os.path.realpath(__file__))
check_scenarios_directory = os.path.join(current_directory, "test_scenarios")
# python2 and python3 checks extension
py2_check_scenarios_directory = os.path.join(check_scenarios_directory, "py2_test_scenarios")
py3_check_scenarios_directory = os.path.join(check_scenarios_directory, "py3_test_scenarios")
test_packages_directory = os.path.join(current_directory, "packages")
test_check_absolute_paths = [os.path.join(check_scenarios_directory, file)
                             for file in os.listdir(check_scenarios_directory)
                             if os.path.isfile(os.path.join(check_scenarios_directory, file))]
# append py2 or py3 exclusive test scenarios
if six.PY2:
    test_check_absolute_paths += [os.path.join(py2_check_scenarios_directory, file)
                                  for file in os.listdir(py2_check_scenarios_directory)
                                  if os.path.isfile(os.path.join(py2_check_scenarios_directory, file))]
else:
    test_check_absolute_paths += [os.path.join(py3_check_scenarios_directory, file)
                                  for file in os.listdir(py3_check_scenarios_directory)
                                  if os.path.isfile(os.path.join(py3_check_scenarios_directory, file))]

@pytest.fixture()
def all_package_paths():
    return os.listdir(test_packages_directory)


@pytest.fixture()
def all_test_scenarios(scenarios_files_to_return=None):
    """Returns returns all the contents of each scenario file as a list of 
    dictionaries

    :param scenarios_files_to_return the names of each scenario files contents to 
    return if empty will return all
    """
    scenarios_files_to_return = scenarios_files_to_return or []
    all_scenarios = []

    for file in test_check_absolute_paths:
        filename = os.path.basename(file)
        with open(file) as csvfile:
            for row in csv.DictReader(csvfile):
                row["filename"] = filename
                all_scenarios.append(row)

    if scenarios_files_to_return:
        all_scenarios = [scenario
                         for scenario
                         in all_scenarios
                         if scenario[filename] in scenarios_files_to_return]

    return all_scenarios


@pytest.fixture()
def all_test_scenarios_packages(all_test_scenarios):
    return set([test_scenario["package"]
                for test_scenario
                in all_test_scenarios])


# Generates a dictionary for eachgroup with its respective checks and
# tracks the number of times each check is tested
@pytest.fixture()
def check_test_counts():
    # Might be a little confusing - Makes a dictionary that returns a function
    # when a key isn't found. Then that function returns another
    # default dictionary that returns an integer as a default value. Used to
    # make it so that it's a dictionary with dictionaries as its values, and
    # those dictionaries contain integer as the default value.
    def create_default_dict_with_int():
        return collections.defaultdict(int)

    check_test_counts = collections.defaultdict(create_default_dict_with_int)
    for file in test_check_absolute_paths:
        filename = os.path.basename(file)
        # removed the test_prefix from the filename
        group_name = re.sub("test_", "", os.path.splitext(filename)[0])
        with open(file) as csvfile:
            for row in csv.DictReader(csvfile):
                check_name = row['check']
                check_test_counts[group_name][check_name] += 1
    return check_test_counts


def check_package_files_tuples():
    """Returns a dictionary with the name of a check as the key and a dictionary
    as the value.

    The nested dictionary contains keys that are the tuple of name of the
    test package uses to validate the check and the testing platform, e.g. (package_name, platorm).
    And the value is an array of the files that contain these check tests. 

    If the array is greater than the length of 1 then that test has been
    duplicated.
    """
    def create_default_dict_with_array():
        return collections.defaultdict(lambda: [])

    check_package_list = collections.defaultdict(create_default_dict_with_array)

    for file in test_check_absolute_paths:
        filename = os.path.basename(file)
        with open(file) as csvfile:
            for row in csv.DictReader(csvfile):
                package_name = row['package']
                check_name = row['check']
                if row['platform'] is None:
                    row['platform'] = ""
                if row['included_tags'] is None:
                    row['included_tags'] = ""
                check_package_list[check_name][(package_name, row['platform'], row['included_tags'])].append(filename)
    output_tuple_list = [(check_name, package_name, files_using_package)
                         for check_name, package_name_dict
                         in iteritems(check_package_list)
                         for package_name, files_using_package
                         in iteritems(package_name_dict)]
    return output_tuple_list


@pytest.mark.parametrize("group_and_check_tuple", group_and_check_tuples)
def test_that_checks_are_tested(group_and_check_tuple, check_test_counts):
    """Tests that for each check in a group there exists at least one or more
    tests validating it.
    """
    group_name = group_and_check_tuple[0]
    check_name = group_and_check_tuple[1]
    log_output = "Checking that group '{}' has check '{}'".format(group_name,
                                                                  check_name)
    logger.debug(log_output)
    if check_test_counts[group_name][check_name] == 0:
        output_string = "{},{} has no tests".format(group_name, check_name)
        pytest.fail(output_string, pytrace=False)


@pytest.mark.parametrize("check_package_files_tuple", check_package_files_tuples())
def test_for_duplicate_tests(check_package_files_tuple):
    """Tests that for each check it is only tested with a specific package and
    specific included_tags under a specific platform once.

    This has been programmed such that it will detect duplicate checks across 
    multiple files, however if test creation is performed right it should only 
    detect duplicates in the same file.
    """
    (check_name, package_name, files_using_package) = check_package_files_tuple
    if len(files_using_package) > 1:
        pytest_output = ("A check has been found with a duplicated test"
                         " package. This means that the same test is being"
                         " performed twice and is un-needed. Please remove the"
                         " duplicate test."
                         " Test: {},{}"
                         " Files: {}"
                         ).format(package_name, check_name, files_using_package)
        pytest.fail(pytest_output, pytrace=False)


@pytest.mark.parametrize("package_name", all_package_paths())
def test_for_unused_packages(all_test_scenarios_packages, package_name):
    """Test that each package is used. """
    # The paths in scenario files can be relative, so the assumption is to look
    # to see if the root path is used in the scenario files, rather than do
    # a full path match
    all_test_scenarios_packages_root = [test_scenario_package.split("/")[0]
                                        for test_scenario_package
                                        in all_test_scenarios_packages]
    package_white_list = ["app_package_testing_packages"]
    if (package_name not in all_test_scenarios_packages_root and
            package_name not in package_white_list):
        pytest_output = ("An unused package was detected. Please add a test for"
                         " it, or remove it from the code base."
                         " Package: {}"
                         ).format(package_name)
        pytest.fail(pytest_output, pytrace=False)
