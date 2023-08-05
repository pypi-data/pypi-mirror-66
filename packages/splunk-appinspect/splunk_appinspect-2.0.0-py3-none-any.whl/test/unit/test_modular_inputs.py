"""Module for testing the Splunk AppInspect App object."""

# Python Standard Libraries
import os

# Third-Party Libraries
import pytest

# Custom Libraries
import splunk_appinspect

APPINSPECT_TEST_PATH = os.path.dirname(os.path.abspath(__file__))
APPINSPECT_TEST_PACKAGES_PATH = os.path.join(APPINSPECT_TEST_PATH, "packages")
APP_PACKAGE_TESTING_PACKAGES_PATH = os.path.join(APPINSPECT_TEST_PACKAGES_PATH, "app_package_testing_packages")

CAMEL_CASE_SENSITIVITY_PACKAGE_PATH = os.path.join(APP_PACKAGE_TESTING_PACKAGES_PATH,
                                                   "has_modular_input_with_camel_case_arg_in_spec-ACD-2937")
LOWER_CASE_SENSITIVITY_PACKAGE_PATH = os.path.join(APP_PACKAGE_TESTING_PACKAGES_PATH,
                                                     "has_modular_input_with_lower_case_arg_in_spec-ACD-2937")


expected_modular_inputs_check_args_case_sensitive_result = (
    (CAMEL_CASE_SENSITIVITY_PACKAGE_PATH, True),
    (LOWER_CASE_SENSITIVITY_PACKAGE_PATH, True),
)


@pytest.mark.parametrize("test_package_path,expected_case_sensitive_check_result",
                         expected_modular_inputs_check_args_case_sensitive_result)
def test_app_modular_inputs_has_correct_option_in_conf_spec(test_package_path, expected_case_sensitive_check_result):
    """Test app package modular inputs objects has exactly the same arg, case sensitive
    """
    app = splunk_appinspect.App(test_package_path)
    modular_inputs = app.get_modular_inputs()
    if modular_inputs.has_specification_file():
        parsed_spec_file = modular_inputs.get_specification_file()

        for mod_input in modular_inputs.get_modular_inputs():
            for mod_input_arg in mod_input.args:
                assert (parsed_spec_file.has_option(mod_input.full_name, mod_input_arg)
                        is expected_case_sensitive_check_result)
    else:
        assert False


def test_find_exes_only_in_bin_directory_and_not_in_sub_directories():
    test_pkg_path = os.path.join(APP_PACKAGE_TESTING_PACKAGES_PATH, "test_find_exes-ACD-3289")
    app = splunk_appinspect.App(test_pkg_path)
    modular_inputs = app.get_modular_inputs()
    exes = list(modular_inputs.find_exes(name="geoipupdate"))
    assert len(exes) == 1
    finding = exes[0].file_path.replace(app.app_dir + os.path.sep, "")
    assert finding == "bin" + os.path.sep + "geoipupdate.py"
