"""A module for testing the AppPackage class."""

# Python Standard Libraries
import os
import shutil
import stat
import tarfile
import tempfile
# Third-Party Libraries
import mock
import pytest
# Custom Libraries
import splunk_appinspect

APPINSPECT_TEST_PATH = os.path.dirname(os.path.abspath(__file__))
APPINSPECT_TEST_PACKAGES_PATH = os.path.join(APPINSPECT_TEST_PATH, "packages")
APP_PACKAGE_TESTING_PACKAGES_PATH = os.path.join(APPINSPECT_TEST_PACKAGES_PATH, "app_package_testing_packages")


# ==============================================================================
# factory function testing
# ==============================================================================
app_package_factory_test_parameters = [
    (os.path.join(APPINSPECT_TEST_PACKAGES_PATH, "good_app_conf"), splunk_appinspect.app_package_handler.FolderAppPackage),
    (os.path.join(APP_PACKAGE_TESTING_PACKAGES_PATH, "good_app_conf.spl"), splunk_appinspect.app_package_handler.TarAppPackage),
    (os.path.join(APP_PACKAGE_TESTING_PACKAGES_PATH, "good_app_conf.tgz"), splunk_appinspect.app_package_handler.TarAppPackage),
    (os.path.join(APP_PACKAGE_TESTING_PACKAGES_PATH, "good_app_conf.tar.gz"), splunk_appinspect.app_package_handler.TarAppPackage),
    (os.path.join(APP_PACKAGE_TESTING_PACKAGES_PATH, "good_app_conf.zip"), splunk_appinspect.app_package_handler.ZipAppPackage),
    (os.path.join(APP_PACKAGE_TESTING_PACKAGES_PATH, "has_nested_good_tgz_spl_zip_splunk_apps-ACD-1310"), splunk_appinspect.app_package_handler.FolderAppPackage),
    (os.path.join(APP_PACKAGE_TESTING_PACKAGES_PATH, "has_nested_good_tgz_spl_zip_splunk_apps-ACD-1310.tgz"), splunk_appinspect.app_package_handler.TarAppPackage),
]


@pytest.mark.parametrize("test_package_path,expected_package_factory_type", app_package_factory_test_parameters)
def test_app_package_factory(test_package_path, expected_package_factory_type):
    """A test to determine that output objects of the AppPackage.factory
    functions are being correctly returned.
    """
    app_package = splunk_appinspect.app_package_handler.AppPackage.factory(test_package_path)
    app_package.clean_up()
    assert isinstance(app_package,
                      expected_package_factory_type)


# ==============================================================================
# is_origin_artifact_valid_compressed_file testing
# ==============================================================================
is_origin_artifact_valid_compressed_file_test_parameters = [
    # Invalid - Packages are 0 bytes
    (os.path.join(APP_PACKAGE_TESTING_PACKAGES_PATH, "invalid_spl_file-ACD-1682.spl"), False),
    (os.path.join(APP_PACKAGE_TESTING_PACKAGES_PATH, "invalid_tar_file-ACD-1682.tgz"), False),
    (os.path.join(APP_PACKAGE_TESTING_PACKAGES_PATH, "invalid_tar_file-ACD-1682.tar.gz"), False),
    (os.path.join(APP_PACKAGE_TESTING_PACKAGES_PATH, "invalid_zip_file-ACD-1682.zip"), False),
    # Invalid - Traversal attack attempts to extract to absolute path
    # /etc/passwd1 created using `tar -cPf foo.tar /etc/passwd1`
    (os.path.join(APP_PACKAGE_TESTING_PACKAGES_PATH, "traversal_attack_to_etc_passwd1.tgz"), False),
    (os.path.join(APP_PACKAGE_TESTING_PACKAGES_PATH, "traversal_attack_to_etc_passwd1.tar.gz"), False),
    # Invalid - Traversal attack attempts to extract to relative path
    # ../../badfile created using `tar -cPf foo.tar ../../badfile`
    (os.path.join(APP_PACKAGE_TESTING_PACKAGES_PATH, "traversal_attack_relative_path_two_levels_back.tgz"), False),
    (os.path.join(APP_PACKAGE_TESTING_PACKAGES_PATH, "traversal_attack_relative_path_two_levels_back.tar.gz"), False),
    # Valid
    (os.path.join(APPINSPECT_TEST_PACKAGES_PATH, "good_app_conf"), True),
    (os.path.join(APP_PACKAGE_TESTING_PACKAGES_PATH, "good_app_conf.spl"), True),
    (os.path.join(APP_PACKAGE_TESTING_PACKAGES_PATH, "good_app_conf.tar.gz"), True),
    (os.path.join(APP_PACKAGE_TESTING_PACKAGES_PATH, "good_app_conf.tgz"), True),
    (os.path.join(APP_PACKAGE_TESTING_PACKAGES_PATH, "good_app_conf.zip"), True),
    (os.path.join(APP_PACKAGE_TESTING_PACKAGES_PATH, "has_nested_good_tgz_spl_zip_splunk_apps-ACD-1310"), True),
    (os.path.join(APP_PACKAGE_TESTING_PACKAGES_PATH, "has_nested_good_tgz_spl_zip_splunk_apps-ACD-1310.tgz"), True),
    (os.path.join(APP_PACKAGE_TESTING_PACKAGES_PATH, "has_hidden_dependencies_directory-ACD-1556"), True),
    (os.path.join(APP_PACKAGE_TESTING_PACKAGES_PATH, "has_hidden_dependencies_directory-ACD-1556.spl"), True),
    (os.path.join(APP_PACKAGE_TESTING_PACKAGES_PATH, "has_hidden_dependencies_directory-ACD-1556.tar.gz"), True),
    (os.path.join(APP_PACKAGE_TESTING_PACKAGES_PATH, "has_hidden_dependencies_directory-ACD-1556.tgz"), True),
    (os.path.join(APP_PACKAGE_TESTING_PACKAGES_PATH, "has_hidden_dependencies_directory-ACD-1556.zip"), True),
]


@pytest.mark.parametrize("test_package_path,expected_result", is_origin_artifact_valid_compressed_file_test_parameters)
def test_is_origin_artifact_valid_compressed_file(test_package_path, expected_result):
    """A test to determine that the initial package provided is correctly being
    detected as:
        - being able to extract correctly.
    """
    app_package = splunk_appinspect.app_package_handler.AppPackage.factory(test_package_path)
    is_origin_artifact_valid_compressed_file = app_package.is_origin_artifact_valid_compressed_file()
    assertion_output = ("The package `{}` for the function"
                        " `is_origin_artifact_valid_compressed_file() `"
                        " expected the result `{}`, but received `{}`"
                        ).format(test_package_path,
                                 expected_result,
                                 is_origin_artifact_valid_compressed_file)
    app_package.clean_up()
    assert is_origin_artifact_valid_compressed_file == expected_result, assertion_output


# ==============================================================================
# is_origin_artifact_a_splunk_app testing
# ==============================================================================
is_origin_artifact_a_splunk_app_test_parameters = [
    # Invalid - Packages that start with a `.`
    (os.path.join(APP_PACKAGE_TESTING_PACKAGES_PATH, ".is_a_hidden_directory_package-ACD-1362"), False),
    (os.path.join(APP_PACKAGE_TESTING_PACKAGES_PATH, ".is_a_hidden_spl_package-ACD-1362.spl"), False),
    (os.path.join(APP_PACKAGE_TESTING_PACKAGES_PATH, ".is_a_hidden_tar_gz_package-ACD-1362.tar.gz"), False),
    (os.path.join(APP_PACKAGE_TESTING_PACKAGES_PATH, ".is_a_hidden_tgz_package-ACD-1362.tgz"), False),
    (os.path.join(APP_PACKAGE_TESTING_PACKAGES_PATH, ".is_a_hidden_zip_package-ACD-1362.zip"), False),
    # Invalid - Packages are 0 bytes
    (os.path.join(APP_PACKAGE_TESTING_PACKAGES_PATH, "invalid_spl_file-ACD-1682.spl"), False),
    (os.path.join(APP_PACKAGE_TESTING_PACKAGES_PATH, "invalid_tar_file-ACD-1682.tgz"), False),
    (os.path.join(APP_PACKAGE_TESTING_PACKAGES_PATH, "invalid_tar_file-ACD-1682.tar.gz"), False),
    (os.path.join(APP_PACKAGE_TESTING_PACKAGES_PATH, "invalid_zip_file-ACD-1682.zip"), False),
    # Invalid - Traversal attack attempts to extract to absolute path /etc/passwd1
    (os.path.join(APP_PACKAGE_TESTING_PACKAGES_PATH, "traversal_attack_to_etc_passwd1.tgz"), False),
    (os.path.join(APP_PACKAGE_TESTING_PACKAGES_PATH, "traversal_attack_to_etc_passwd1.tar.gz"), False),
    # Invalid - Traversal attack attempts to extract to relative path
    # ../../badfile created using `tar -cPf foo.tar ../../badfile`
    (os.path.join(APP_PACKAGE_TESTING_PACKAGES_PATH, "traversal_attack_relative_path_two_levels_back.tgz"), False),
    (os.path.join(APP_PACKAGE_TESTING_PACKAGES_PATH, "traversal_attack_relative_path_two_levels_back.tar.gz"), False),
    # Valid
    (os.path.join(APPINSPECT_TEST_PACKAGES_PATH, "good_app_conf"), True),
    (os.path.join(APP_PACKAGE_TESTING_PACKAGES_PATH, "good_app_conf.spl"), True),
    (os.path.join(APP_PACKAGE_TESTING_PACKAGES_PATH, "good_app_conf.tar.gz"), True),
    (os.path.join(APP_PACKAGE_TESTING_PACKAGES_PATH, "good_app_conf.tgz"), True),
    (os.path.join(APP_PACKAGE_TESTING_PACKAGES_PATH, "good_app_conf.zip"), True),
    (os.path.join(APP_PACKAGE_TESTING_PACKAGES_PATH, "has_nested_good_tgz_spl_zip_splunk_apps-ACD-1310"), True),
    (os.path.join(APP_PACKAGE_TESTING_PACKAGES_PATH, "has_nested_good_tgz_spl_zip_splunk_apps-ACD-1310.tgz"), True),
    (os.path.join(APP_PACKAGE_TESTING_PACKAGES_PATH, "has_hidden_dependencies_directory-ACD-1556"), True),
    (os.path.join(APP_PACKAGE_TESTING_PACKAGES_PATH, "has_hidden_dependencies_directory-ACD-1556.spl"), True),
    (os.path.join(APP_PACKAGE_TESTING_PACKAGES_PATH, "has_hidden_dependencies_directory-ACD-1556.tar.gz"), True),
    (os.path.join(APP_PACKAGE_TESTING_PACKAGES_PATH, "has_hidden_dependencies_directory-ACD-1556.tgz"), True),
    (os.path.join(APP_PACKAGE_TESTING_PACKAGES_PATH, "has_hidden_dependencies_directory-ACD-1556.zip"), True),
]


@pytest.mark.parametrize("test_package_path,expected_result", is_origin_artifact_a_splunk_app_test_parameters)
def test_is_origin_artifact_a_splunk_app(test_package_path, expected_result):
    """A test to determine that the initial package provided is correctly being
    detected as a Splunk App.
    """
    app_package = splunk_appinspect.app_package_handler.AppPackage.factory(test_package_path)
    is_origin_artifact_a_splunk_app = app_package.is_origin_artifact_a_splunk_app()
    assertion_output = ("The package `{}` for the function"
                        " `is_origin_artifact_a_splunk_app() `"
                        " expected the result `{}`, but received `{}`"
                        ).format(test_package_path,
                                 expected_result,
                                 is_origin_artifact_a_splunk_app)
    app_package.clean_up()
    assert is_origin_artifact_a_splunk_app == expected_result, assertion_output


# ==============================================================================
# is_working_artifact_a_splunk_app testing
# ==============================================================================
is_working_artifact_a_splunk_app_test_parameters = [
    # Has a package that when extracted is a file
    (os.path.join(APP_PACKAGE_TESTING_PACKAGES_PATH, "extracts_to_file-ACD-1556.spl"), False),
    (os.path.join(APP_PACKAGE_TESTING_PACKAGES_PATH, "extracts_to_file-ACD-1556.tar.gz"), False),
    (os.path.join(APP_PACKAGE_TESTING_PACKAGES_PATH, "extracts_to_file-ACD-1556.tgz"), False),
    (os.path.join(APP_PACKAGE_TESTING_PACKAGES_PATH, "extracts_to_file-ACD-1556.zip"), False),
    # Has a package that when extracted starts with a `.`
    (os.path.join(APP_PACKAGE_TESTING_PACKAGES_PATH, ".has_package_name_that_is_hidden_directory-ACD-1362"), False),
    (os.path.join(APP_PACKAGE_TESTING_PACKAGES_PATH, "has_package_name_that_is_hidden_directory-ACD-1362.tgz"), False),
    (os.path.join(APP_PACKAGE_TESTING_PACKAGES_PATH, "has_package_name_that_is_hidden_directory-ACD-1362.tar.gz"), False),
    (os.path.join(APP_PACKAGE_TESTING_PACKAGES_PATH, "has_package_name_that_is_hidden_directory-ACD-1362.spl"), False),
    (os.path.join(APP_PACKAGE_TESTING_PACKAGES_PATH, "has_package_name_that_is_hidden_directory-ACD-1362.zip"), False),
    # Has a package that contains a __MACOSX file
    (os.path.join(APP_PACKAGE_TESTING_PACKAGES_PATH, "has_macosx_directory-ACD-1362"), False),
    (os.path.join(APP_PACKAGE_TESTING_PACKAGES_PATH, "has_macosx_directory-ACD-1362.spl"), False),
    (os.path.join(APP_PACKAGE_TESTING_PACKAGES_PATH, "has_macosx_directory-ACD-1362.tar.gz"), False),
    (os.path.join(APP_PACKAGE_TESTING_PACKAGES_PATH, "has_macosx_directory-ACD-1362.tgz"), False),
    (os.path.join(APP_PACKAGE_TESTING_PACKAGES_PATH, "has_macosx_directory-ACD-1362.zip"), False),
    # Has a package that contains a hidden directory
    (os.path.join(APP_PACKAGE_TESTING_PACKAGES_PATH, "has_hidden_directory-ACD-1362"), False),
    (os.path.join(APP_PACKAGE_TESTING_PACKAGES_PATH, "has_hidden_directory-ACD-1362.spl"), False),
    (os.path.join(APP_PACKAGE_TESTING_PACKAGES_PATH, "has_hidden_directory-ACD-1362.tar.gz"), False),
    (os.path.join(APP_PACKAGE_TESTING_PACKAGES_PATH, "has_hidden_directory-ACD-1362.tgz"), False),
    (os.path.join(APP_PACKAGE_TESTING_PACKAGES_PATH, "has_hidden_directory-ACD-1362.zip"), False),
    # Has no app.conf file in the extracted package
    (os.path.join(APP_PACKAGE_TESTING_PACKAGES_PATH, "has_missing_app_conf_file-ACD-1362"), False),
    (os.path.join(APP_PACKAGE_TESTING_PACKAGES_PATH, "has_missing_app_conf_file-ACD-1362.spl"), False),
    (os.path.join(APP_PACKAGE_TESTING_PACKAGES_PATH, "has_missing_app_conf_file-ACD-1362.tar.gz"), False),
    (os.path.join(APP_PACKAGE_TESTING_PACKAGES_PATH, "has_missing_app_conf_file-ACD-1362.tgz"), False),
    (os.path.join(APP_PACKAGE_TESTING_PACKAGES_PATH, "has_missing_app_conf_file-ACD-1362.zip"), False),
    # Nested valid apps, but main structure is not considered valid
    (os.path.join(APP_PACKAGE_TESTING_PACKAGES_PATH, "has_nested_good_tgz_spl_zip_splunk_apps-ACD-1310"), False),
    (os.path.join(APP_PACKAGE_TESTING_PACKAGES_PATH, "has_nested_good_tgz_spl_zip_splunk_apps-ACD-1310.tgz"), False),
    # Valid apps
    (os.path.join(APPINSPECT_TEST_PACKAGES_PATH, "good_app_conf"), True),
    (os.path.join(APP_PACKAGE_TESTING_PACKAGES_PATH, "good_app_conf.spl"), True),
    (os.path.join(APP_PACKAGE_TESTING_PACKAGES_PATH, "good_app_conf.tar.gz"), True),
    (os.path.join(APP_PACKAGE_TESTING_PACKAGES_PATH, "good_app_conf.tgz"), True),
    (os.path.join(APP_PACKAGE_TESTING_PACKAGES_PATH, "good_app_conf.zip"), True),
    (os.path.join(APP_PACKAGE_TESTING_PACKAGES_PATH, "has_hidden_dependencies_directory-ACD-1556"), True),
    (os.path.join(APP_PACKAGE_TESTING_PACKAGES_PATH, "has_hidden_dependencies_directory-ACD-1556", "has_hidden_dependencies_directory-ACD-1556"), True),
    (os.path.join(APP_PACKAGE_TESTING_PACKAGES_PATH, "has_hidden_dependencies_directory-ACD-1556.spl"), True),
    (os.path.join(APP_PACKAGE_TESTING_PACKAGES_PATH, "has_hidden_dependencies_directory-ACD-1556.tar.gz"), True),
    (os.path.join(APP_PACKAGE_TESTING_PACKAGES_PATH, "has_hidden_dependencies_directory-ACD-1556.tgz"), True),
    (os.path.join(APP_PACKAGE_TESTING_PACKAGES_PATH, "has_hidden_dependencies_directory-ACD-1556.zip"), True),
]


@pytest.mark.parametrize("test_package_path,expected_result", is_working_artifact_a_splunk_app_test_parameters)
def test_is_working_artifact_a_splunk_app(test_package_path, expected_result):
    """A test to determine that the app extracted from the initial package
    provided is correctly being detected as a Splunk App.
    """
    app_package = splunk_appinspect.app_package_handler.AppPackage.factory(test_package_path)
    is_working_artifact_a_splunk_app = app_package.is_working_artifact_a_splunk_app()
    assertion_output = ("The package `{}` for the function"
                        " `is_working_artifact_a_splunk_app() `"
                        " expected the result `{}`, but received `{}`"
                        ).format(test_package_path,
                                 expected_result,
                                 is_working_artifact_a_splunk_app)
    app_package.clean_up()
    assert is_working_artifact_a_splunk_app == expected_result, assertion_output


# ==============================================================================
# is_splunk_app testing
# ==============================================================================
is_splunk_app_test_parameters = [
    # Origin artifacts
    # Invalid - Packages that start with a `.`
    (os.path.join(APP_PACKAGE_TESTING_PACKAGES_PATH, ".is_a_hidden_directory_package-ACD-1362"), False),
    (os.path.join(APP_PACKAGE_TESTING_PACKAGES_PATH, ".is_a_hidden_spl_package-ACD-1362.spl"), False),
    (os.path.join(APP_PACKAGE_TESTING_PACKAGES_PATH, ".is_a_hidden_tar_gz_package-ACD-1362.tar.gz"), False),
    (os.path.join(APP_PACKAGE_TESTING_PACKAGES_PATH, ".is_a_hidden_tgz_package-ACD-1362.tgz"), False),
    (os.path.join(APP_PACKAGE_TESTING_PACKAGES_PATH, ".is_a_hidden_zip_package-ACD-1362.zip"), False),
    # Valid
    (os.path.join(APPINSPECT_TEST_PACKAGES_PATH, "good_app_conf"), True),
    (os.path.join(APP_PACKAGE_TESTING_PACKAGES_PATH, "good_app_conf.spl"), True),
    (os.path.join(APP_PACKAGE_TESTING_PACKAGES_PATH, "good_app_conf.tar.gz"), True),
    (os.path.join(APP_PACKAGE_TESTING_PACKAGES_PATH, "good_app_conf.tgz"), True),
    (os.path.join(APP_PACKAGE_TESTING_PACKAGES_PATH, "good_app_conf.zip"), True),
    # Working artifacts
    # Invalid - Has a package that when extracted is a file
    (os.path.join(APP_PACKAGE_TESTING_PACKAGES_PATH, "extracts_to_file-ACD-1556.spl"), False),
    (os.path.join(APP_PACKAGE_TESTING_PACKAGES_PATH, "extracts_to_file-ACD-1556.tar.gz"), False),
    (os.path.join(APP_PACKAGE_TESTING_PACKAGES_PATH, "extracts_to_file-ACD-1556.tgz"), False),
    (os.path.join(APP_PACKAGE_TESTING_PACKAGES_PATH, "extracts_to_file-ACD-1556.zip"), False),
    # Invalid - Has a package that when extracted starts with a `.`
    (os.path.join(APP_PACKAGE_TESTING_PACKAGES_PATH, ".has_package_name_that_is_hidden_directory-ACD-1362"), False),
    (os.path.join(APP_PACKAGE_TESTING_PACKAGES_PATH, "has_package_name_that_is_hidden_directory-ACD-1362.tgz"), False),
    (os.path.join(APP_PACKAGE_TESTING_PACKAGES_PATH, "has_package_name_that_is_hidden_directory-ACD-1362.tar.gz"), False),
    (os.path.join(APP_PACKAGE_TESTING_PACKAGES_PATH, "has_package_name_that_is_hidden_directory-ACD-1362.spl"), False),
    (os.path.join(APP_PACKAGE_TESTING_PACKAGES_PATH, "has_package_name_that_is_hidden_directory-ACD-1362.zip"), False),
    # Invalid - Has a package that contains a __MACOSX file
    (os.path.join(APP_PACKAGE_TESTING_PACKAGES_PATH, "has_macosx_directory-ACD-1362"), False),
    (os.path.join(APP_PACKAGE_TESTING_PACKAGES_PATH, "has_macosx_directory-ACD-1362.spl"), False),
    (os.path.join(APP_PACKAGE_TESTING_PACKAGES_PATH, "has_macosx_directory-ACD-1362.tar.gz"), False),
    (os.path.join(APP_PACKAGE_TESTING_PACKAGES_PATH, "has_macosx_directory-ACD-1362.tgz"), False),
    (os.path.join(APP_PACKAGE_TESTING_PACKAGES_PATH, "has_macosx_directory-ACD-1362.zip"), False),
    # Invalid- Has a package that contains a hidden directory
    (os.path.join(APP_PACKAGE_TESTING_PACKAGES_PATH, "has_hidden_directory-ACD-1362"), False),
    (os.path.join(APP_PACKAGE_TESTING_PACKAGES_PATH, "has_hidden_directory-ACD-1362.spl"), False),
    (os.path.join(APP_PACKAGE_TESTING_PACKAGES_PATH, "has_hidden_directory-ACD-1362.tar.gz"), False),
    (os.path.join(APP_PACKAGE_TESTING_PACKAGES_PATH, "has_hidden_directory-ACD-1362.tgz"), False),
    (os.path.join(APP_PACKAGE_TESTING_PACKAGES_PATH, "has_hidden_directory-ACD-1362.zip"), False),
    # Invalid- Has no app.conf file in the extracted package
    (os.path.join(APP_PACKAGE_TESTING_PACKAGES_PATH, "has_missing_app_conf_file-ACD-1362"), False),
    (os.path.join(APP_PACKAGE_TESTING_PACKAGES_PATH, "has_missing_app_conf_file-ACD-1362.spl"), False),
    (os.path.join(APP_PACKAGE_TESTING_PACKAGES_PATH, "has_missing_app_conf_file-ACD-1362.tar.gz"), False),
    (os.path.join(APP_PACKAGE_TESTING_PACKAGES_PATH, "has_missing_app_conf_file-ACD-1362.tgz"), False),
    (os.path.join(APP_PACKAGE_TESTING_PACKAGES_PATH, "has_missing_app_conf_file-ACD-1362.zip"), False),
    # Invalid - Packages are 0 bytes
    (os.path.join(APP_PACKAGE_TESTING_PACKAGES_PATH, "invalid_spl_file-ACD-1682.spl"), False),
    (os.path.join(APP_PACKAGE_TESTING_PACKAGES_PATH, "invalid_tar_file-ACD-1682.tgz"), False),
    (os.path.join(APP_PACKAGE_TESTING_PACKAGES_PATH, "invalid_tar_file-ACD-1682.tar.gz"), False),
    (os.path.join(APP_PACKAGE_TESTING_PACKAGES_PATH, "invalid_zip_file-ACD-1682.zip"), False),
    # Invalid - Traversal attack attempts to extract to absolute path
    # /etc/passwd1 created using `tar -cPf foo.tar /etc/passwd1`
    (os.path.join(APP_PACKAGE_TESTING_PACKAGES_PATH, "traversal_attack_to_etc_passwd1.tgz"), False),
    (os.path.join(APP_PACKAGE_TESTING_PACKAGES_PATH, "traversal_attack_to_etc_passwd1.tar.gz"), False),
    # Invalid - Traversal attack attempts to extract to relative path
    # ../../badfile created using `tar -cPf foo.tar ../../badfile`
    (os.path.join(APP_PACKAGE_TESTING_PACKAGES_PATH, "traversal_attack_relative_path_two_levels_back.tgz"), False),
    (os.path.join(APP_PACKAGE_TESTING_PACKAGES_PATH, "traversal_attack_relative_path_two_levels_back.tar.gz"), False),
    # Nested valid apps, but main structure is not considered valid
    (os.path.join(APP_PACKAGE_TESTING_PACKAGES_PATH, "has_nested_good_tgz_spl_zip_splunk_apps-ACD-1310"), False),
    (os.path.join(APP_PACKAGE_TESTING_PACKAGES_PATH, "has_nested_good_tgz_spl_zip_splunk_apps-ACD-1310.tgz"), False),
    # Valid apps
    (os.path.join(APPINSPECT_TEST_PACKAGES_PATH, "good_app_conf"), True),
    (os.path.join(APP_PACKAGE_TESTING_PACKAGES_PATH, "good_app_conf.spl"), True),
    (os.path.join(APP_PACKAGE_TESTING_PACKAGES_PATH, "good_app_conf.tar.gz"), True),
    (os.path.join(APP_PACKAGE_TESTING_PACKAGES_PATH, "good_app_conf.tgz"), True),
    (os.path.join(APP_PACKAGE_TESTING_PACKAGES_PATH, "good_app_conf.zip"), True),
    (os.path.join(APP_PACKAGE_TESTING_PACKAGES_PATH, "has_hidden_dependencies_directory-ACD-1556"), True),
    (os.path.join(APP_PACKAGE_TESTING_PACKAGES_PATH, "has_hidden_dependencies_directory-ACD-1556", "has_hidden_dependencies_directory-ACD-1556"), True),
    (os.path.join(APP_PACKAGE_TESTING_PACKAGES_PATH, "has_hidden_dependencies_directory-ACD-1556.spl"), True),
    (os.path.join(APP_PACKAGE_TESTING_PACKAGES_PATH, "has_hidden_dependencies_directory-ACD-1556.tar.gz"), True),
    (os.path.join(APP_PACKAGE_TESTING_PACKAGES_PATH, "has_hidden_dependencies_directory-ACD-1556.tgz"), True),
    (os.path.join(APP_PACKAGE_TESTING_PACKAGES_PATH, "has_hidden_dependencies_directory-ACD-1556.zip"), True),
]


@pytest.mark.parametrize("test_package_path,expected_result", is_splunk_app_test_parameters)
def test_is_splunk_app(test_package_path, expected_result):
    """A test to determine that the both the initial package provided and its
    extracted contents are correctly being detected as a Splunk App.
    """
    app_package = splunk_appinspect.app_package_handler.AppPackage.factory(test_package_path)
    is_splunk_app = app_package.is_splunk_app()
    assertion_output = ("The package `{}` for the function"
                        " `is_splunk_app() `"
                        " expected the result `{}`, but received `{}`"
                        ).format(test_package_path,
                                 expected_result,
                                 is_splunk_app)
    app_package.clean_up()
    assert is_splunk_app == expected_result, assertion_output

# ==============================================================================
# origin_path testing
# ==============================================================================
origin_artifact_path_test_parameters = app_package_factory_test_parameters + is_splunk_app_test_parameters
origin_artifact_path_test_parameters = [(origin_artifact_path_test_parameter[0])
                                        for origin_artifact_path_test_parameter
                                        in origin_artifact_path_test_parameters]


@pytest.mark.parametrize("test_package_path", origin_artifact_path_test_parameters)
def test_origin_path(test_package_path):
    """A test to confirm that the helper functions exposed for getting the name
    of the initial package provided is returning the correct name.
    """
    app_package = splunk_appinspect.app_package_handler.AppPackage.factory(test_package_path)
    origin_artifact_path = app_package.origin_path
    assertion_output = ("The package `{}` for the property"
                        " `origin_artifact_name `"
                        " expected the result `{}`, but received `{}`"
                        ).format(test_package_path,
                                 test_package_path,
                                 origin_artifact_path)
    app_package.clean_up()
    assert origin_artifact_path == test_package_path, assertion_output


origin_artifact_is_valid_compressed_file_test_parameters = [
    # Origin artifacts
    # Invalid - Packages are 0 bytes, should still have the name matching the origin artifact
    (os.path.join(APP_PACKAGE_TESTING_PACKAGES_PATH, "invalid_spl_file-ACD-1682.spl"), False),
    (os.path.join(APP_PACKAGE_TESTING_PACKAGES_PATH, "invalid_tar_file-ACD-1682.tgz"), False),
    (os.path.join(APP_PACKAGE_TESTING_PACKAGES_PATH, "invalid_tar_file-ACD-1682.tar.gz"), False),
    (os.path.join(APP_PACKAGE_TESTING_PACKAGES_PATH, "invalid_zip_file-ACD-1682.zip"), False),
    # Invalid - Traversal attack attempts to extract to absolute path
    # /etc/passwd1 created using `tar -cPf foo.tar /etc/passwd1`
    (os.path.join(APP_PACKAGE_TESTING_PACKAGES_PATH, "traversal_attack_to_etc_passwd1.tgz"), False),
    (os.path.join(APP_PACKAGE_TESTING_PACKAGES_PATH, "traversal_attack_to_etc_passwd1.tar.gz"), False),
    # Invalid - Traversal attack attempts to extract to relative path
    # ../../badfile created using `tar -cPf foo.tar ../../badfile`
    (os.path.join(APP_PACKAGE_TESTING_PACKAGES_PATH, "traversal_attack_relative_path_two_levels_back.tgz"), False),
    (os.path.join(APP_PACKAGE_TESTING_PACKAGES_PATH, "traversal_attack_relative_path_two_levels_back.tar.gz"), False),
    # Valid - these are all either FolderAppPackages or valid compressed files
    # that properly extract and contain no traversal attacks
    (os.path.join(APP_PACKAGE_TESTING_PACKAGES_PATH, ".is_a_hidden_directory_package-ACD-1362"), True),
    (os.path.join(APP_PACKAGE_TESTING_PACKAGES_PATH, ".is_a_hidden_spl_package-ACD-1362.spl"), True),
    (os.path.join(APP_PACKAGE_TESTING_PACKAGES_PATH, ".is_a_hidden_tar_gz_package-ACD-1362.tar.gz"), True),
    (os.path.join(APP_PACKAGE_TESTING_PACKAGES_PATH, ".is_a_hidden_tgz_package-ACD-1362.tgz"), True),
    (os.path.join(APP_PACKAGE_TESTING_PACKAGES_PATH, ".is_a_hidden_zip_package-ACD-1362.zip"), True),
    (os.path.join(APPINSPECT_TEST_PACKAGES_PATH, "good_app_conf"), True),
    (os.path.join(APP_PACKAGE_TESTING_PACKAGES_PATH, "good_app_conf.spl"), True),
    (os.path.join(APP_PACKAGE_TESTING_PACKAGES_PATH, "good_app_conf.tar.gz"), True),
    (os.path.join(APP_PACKAGE_TESTING_PACKAGES_PATH, "good_app_conf.tgz"), True),
    (os.path.join(APP_PACKAGE_TESTING_PACKAGES_PATH, "good_app_conf.zip"), True),
    (os.path.join(APP_PACKAGE_TESTING_PACKAGES_PATH, "extracts_to_file-ACD-1556.spl"), True),
    (os.path.join(APP_PACKAGE_TESTING_PACKAGES_PATH, "extracts_to_file-ACD-1556.tar.gz"), True),
    (os.path.join(APP_PACKAGE_TESTING_PACKAGES_PATH, "extracts_to_file-ACD-1556.tgz"), True),
    (os.path.join(APP_PACKAGE_TESTING_PACKAGES_PATH, "extracts_to_file-ACD-1556.zip"), True),
    (os.path.join(APP_PACKAGE_TESTING_PACKAGES_PATH, ".has_package_name_that_is_hidden_directory-ACD-1362"), True),
    (os.path.join(APP_PACKAGE_TESTING_PACKAGES_PATH, "has_package_name_that_is_hidden_directory-ACD-1362.tgz"), True),
    (os.path.join(APP_PACKAGE_TESTING_PACKAGES_PATH, "has_package_name_that_is_hidden_directory-ACD-1362.tar.gz"), True),
    (os.path.join(APP_PACKAGE_TESTING_PACKAGES_PATH, "has_package_name_that_is_hidden_directory-ACD-1362.spl"), True),
    (os.path.join(APP_PACKAGE_TESTING_PACKAGES_PATH, "has_package_name_that_is_hidden_directory-ACD-1362.zip"), True),
    (os.path.join(APP_PACKAGE_TESTING_PACKAGES_PATH, "has_macosx_directory-ACD-1362"), True),
    (os.path.join(APP_PACKAGE_TESTING_PACKAGES_PATH, "has_macosx_directory-ACD-1362.spl"), True),
    (os.path.join(APP_PACKAGE_TESTING_PACKAGES_PATH, "has_macosx_directory-ACD-1362.tar.gz"), True),
    (os.path.join(APP_PACKAGE_TESTING_PACKAGES_PATH, "has_macosx_directory-ACD-1362.tgz"), True),
    (os.path.join(APP_PACKAGE_TESTING_PACKAGES_PATH, "has_macosx_directory-ACD-1362.zip"), True),
    (os.path.join(APP_PACKAGE_TESTING_PACKAGES_PATH, "has_hidden_directory-ACD-1362"), True),
    (os.path.join(APP_PACKAGE_TESTING_PACKAGES_PATH, "has_hidden_directory-ACD-1362.spl"), True),
    (os.path.join(APP_PACKAGE_TESTING_PACKAGES_PATH, "has_hidden_directory-ACD-1362.tar.gz"), True),
    (os.path.join(APP_PACKAGE_TESTING_PACKAGES_PATH, "has_hidden_directory-ACD-1362.tgz"), True),
    (os.path.join(APP_PACKAGE_TESTING_PACKAGES_PATH, "has_hidden_directory-ACD-1362.zip"), True),
    (os.path.join(APP_PACKAGE_TESTING_PACKAGES_PATH, "has_missing_app_conf_file-ACD-1362"), True),
    (os.path.join(APP_PACKAGE_TESTING_PACKAGES_PATH, "has_missing_app_conf_file-ACD-1362.spl"), True),
    (os.path.join(APP_PACKAGE_TESTING_PACKAGES_PATH, "has_missing_app_conf_file-ACD-1362.tar.gz"), True),
    (os.path.join(APP_PACKAGE_TESTING_PACKAGES_PATH, "has_missing_app_conf_file-ACD-1362.tgz"), True),
    (os.path.join(APP_PACKAGE_TESTING_PACKAGES_PATH, "has_missing_app_conf_file-ACD-1362.zip"), True),
    (os.path.join(APP_PACKAGE_TESTING_PACKAGES_PATH, "has_nested_good_tgz_spl_zip_splunk_apps-ACD-1310"), True),
    (os.path.join(APP_PACKAGE_TESTING_PACKAGES_PATH, "has_nested_good_tgz_spl_zip_splunk_apps-ACD-1310.tgz"), True),
    (os.path.join(APPINSPECT_TEST_PACKAGES_PATH, "good_app_conf"), True),
    (os.path.join(APP_PACKAGE_TESTING_PACKAGES_PATH, "good_app_conf.spl"), True),
    (os.path.join(APP_PACKAGE_TESTING_PACKAGES_PATH, "good_app_conf.tar.gz"), True),
    (os.path.join(APP_PACKAGE_TESTING_PACKAGES_PATH, "good_app_conf.tgz"), True),
    (os.path.join(APP_PACKAGE_TESTING_PACKAGES_PATH, "good_app_conf.zip"), True),
    (os.path.join(APP_PACKAGE_TESTING_PACKAGES_PATH, "has_hidden_dependencies_directory-ACD-1556"), True),
    (os.path.join(APP_PACKAGE_TESTING_PACKAGES_PATH, "has_hidden_dependencies_directory-ACD-1556", "has_hidden_dependencies_directory-ACD-1556"), True),
    (os.path.join(APP_PACKAGE_TESTING_PACKAGES_PATH, "has_hidden_dependencies_directory-ACD-1556.spl"), True),
    (os.path.join(APP_PACKAGE_TESTING_PACKAGES_PATH, "has_hidden_dependencies_directory-ACD-1556.tar.gz"), True),
    (os.path.join(APP_PACKAGE_TESTING_PACKAGES_PATH, "has_hidden_dependencies_directory-ACD-1556.tgz"), True),
    (os.path.join(APP_PACKAGE_TESTING_PACKAGES_PATH, "has_hidden_dependencies_directory-ACD-1556.zip"), True),
]
# ==============================================================================
# is_origin_artifact_valid_compressed_file testing
# ==============================================================================
@pytest.mark.parametrize("test_package_path,is_valid_compressed_file", origin_artifact_is_valid_compressed_file_test_parameters)
def test_app_package_is_origin_artifact_is_valid_compressed_file(test_package_path, is_valid_compressed_file):
    """Tests that the AppPackage.is_origin_artifact_valid_compressed_file()
    returns the expected result. If the package can be successfully extracted
    without traversal attacks then or is a FolderAppPackage then this property
    should be True.
    """
    app_package = splunk_appinspect.app_package_handler.AppPackage.factory(test_package_path)
    assertion_output = ("The package `{}` for the method"
                        " `is_origin_artifact_valid_compressed_file() `"
                        " expected the result `{}`, but received `{}`"
                        ).format(test_package_path,
                                 is_valid_compressed_file,
                                 app_package.is_origin_artifact_valid_compressed_file())
    app_package.clean_up()
    assert is_valid_compressed_file == app_package.is_origin_artifact_valid_compressed_file(), assertion_output


# ==============================================================================
# clean_up() testing
# ==============================================================================
@pytest.mark.parametrize("test_package_path,is_valid_compressed_file", origin_artifact_is_valid_compressed_file_test_parameters)
def test_app_package_cleans_up_temp_directories(test_package_path, is_valid_compressed_file):
    """Tests that the AppPackage class is correctly cleaning up all AppPackages
    including any extracted temp directories.
    """
    tmp_directories_created = []
    unpatched_mkdtemp = tempfile.mkdtemp

    def _mkdtemp_tracker(suffix='', prefix='tmp', _dir=None):
        """Override this method to keep track of any temp directories created
        using tempfile.mkdtemp"""
        temp_dir = unpatched_mkdtemp(suffix, prefix, _dir)
        tmp_directories_created.append(temp_dir)
        return temp_dir

    with mock.patch.object(tempfile, "mkdtemp", new=_mkdtemp_tracker):
        app_package_handler = splunk_appinspect.app_package_handler.AppPackageHandler(test_package_path)

    app_package_handler.cleanup()
    packages_to_test = app_package_handler.app_packages[:]
    if not app_package_handler.origin_package in packages_to_test:
        packages_to_test.append(app_package_handler.origin_package)
    for app_package in packages_to_test:
        if (isinstance(app_package, splunk_appinspect.app_package_handler.CompressedAppPackage) and
                app_package.extracted_path is not None):
            temp_directory_exists = os.path.exists(app_package.extracted_path)
            assertion_output = ("Extracted directory not removed from package:"
                                " `{}` for test_package_path: `{}`".format(
                                app_package.origin_artifact_name,
                                test_package_path))
            assert not temp_directory_exists, assertion_output

    for temp_dir in tmp_directories_created:
        temp_directory_exists = os.path.exists(temp_dir)
        assertion_output = ("Created temp directory not removed from"
                            " package: `{}` for test_package_path: `{}`"
                            .format(app_package.origin_artifact_name,
                            test_package_path))
        assert not temp_directory_exists, assertion_output


@pytest.mark.parametrize("test_package_path,is_valid_compressed_file", origin_artifact_is_valid_compressed_file_test_parameters)
def test_app_package_cleans_up_temp_directories_after_failed_extraction(test_package_path, is_valid_compressed_file):
    """Tests that the AppPackage class is correctly cleaning up all AppPackages
    including any extracted temp directories even when an Exception is raised
    during extraction.
    """
    tmp_directories_created = []
    unpatched_mkdtemp = tempfile.mkdtemp

    def _perform_extraction_raising_exception(self, compressed_application_path, temporary_directory):
        raise Exception()

    def _mkdtemp_tracker(suffix='', prefix='tmp', _dir=None):
        """Override this method to keep track of any temp directories created
        using tempfile.mkdtemp"""
        temp_dir = unpatched_mkdtemp(suffix, prefix, _dir)
        tmp_directories_created.append(temp_dir)
        return temp_dir

    # For CompressedAppPackages, we will raise an exception during extraction
    # to make sure we're still cleaning up properly for this case.
    # NOTE: You have to patch the TarAppPackage and ZipAppPackage individually
    # here, patching the super class (CompressedAppPackage) won't work
    with mock.patch.object(splunk_appinspect.app_package_handler.TarAppPackage,
                           '_perform_extraction', new=_perform_extraction_raising_exception):
        with mock.patch.object(splunk_appinspect.app_package_handler.ZipAppPackage,
                           '_perform_extraction', new=_perform_extraction_raising_exception):
            with mock.patch.object(tempfile, "mkdtemp", new=_mkdtemp_tracker):
                app_package_handler = splunk_appinspect.app_package_handler.AppPackageHandler(
                    test_package_path)

    app_package_handler.cleanup()
    packages_to_test = app_package_handler.app_packages[:]
    if not app_package_handler.origin_package in packages_to_test:
        packages_to_test.append(app_package_handler.origin_package)
    for app_package in packages_to_test:
        if (isinstance(app_package, splunk_appinspect.app_package_handler.CompressedAppPackage) and
                app_package.extracted_path is not None):
            temp_directory_exists = os.path.exists(app_package.extracted_path)
            assertion_output = ("Extracted directory not removed from package:"
                                " `{}` for test_package_path: `{}`".format(
                                app_package.origin_artifact_name,
                                test_package_path))
            assert not temp_directory_exists, assertion_output

    for temp_dir in tmp_directories_created:
        temp_directory_exists = os.path.exists(temp_dir)
        assertion_output = ("Created temp directory not removed from"
                            " package: `{}` for test_package_path: `{}`"
                            .format(app_package.origin_artifact_name,
                            test_package_path))
        assert not temp_directory_exists, assertion_output


@pytest.mark.parametrize("test_package_path,expected_result", is_origin_artifact_valid_compressed_file_test_parameters)
def test_generate_app_package_from_file_or_folder_invalid_packages_are_cleaned_up(test_package_path, expected_result):
    """Tests that AppPackage.generate_app_package_from_file_or_folder() cleans
    up temp directories for artifacts that are not valid.
    """
    tmp_directories_created = []
    unpatched_mkdtemp = tempfile.mkdtemp

    def _mkdtemp_tracker(suffix='', prefix='tmp', _dir=None):
        """Override this method to keep track of any temp directories created
        using tempfile.mkdtemp"""
        temp_dir = unpatched_mkdtemp(suffix, prefix, _dir)
        tmp_directories_created.append(temp_dir)
        return temp_dir

    app_package = None
    with mock.patch.object(tempfile, "mkdtemp", new=_mkdtemp_tracker):
        app_package = splunk_appinspect.app_package_handler.AppPackage.generate_app_package_from_file_or_folder(
            test_package_path)

    if app_package is not None:
        # Valid packages should be retained, not cleaned up
        return

    for temp_dir in tmp_directories_created:
        temp_directory_exists = os.path.exists(temp_dir)
        assertion_output = ("Created temp directory not removed from"
                            " package for test_package_path: `{}`"
                            .format(test_package_path))
        assert not temp_directory_exists, assertion_output


origin_artifact_traversal_attack_exists_test_parameters = [
    # Origin artifacts
    # Invalid - Traversal attack attempts to extract to absolute path
    # /etc/passwd1 created using `tar -cPf foo.tar /etc/passwd1`
    (os.path.join(APP_PACKAGE_TESTING_PACKAGES_PATH, "traversal_attack_to_etc_passwd1.tgz"), True),
    (os.path.join(APP_PACKAGE_TESTING_PACKAGES_PATH, "traversal_attack_to_etc_passwd1.tar.gz"), True),
    # Invalid - Traversal attack attempts to extract to relative path
    # ../../badfile created using `tar -cPf foo.tar ../../badfile`
    (os.path.join(APP_PACKAGE_TESTING_PACKAGES_PATH, "traversal_attack_relative_path_two_levels_back.tgz"), True),
    (os.path.join(APP_PACKAGE_TESTING_PACKAGES_PATH, "traversal_attack_relative_path_two_levels_back.tar.gz"), True),
    # Invalid - Packages are 0 bytes but no traversal attack
    (os.path.join(APP_PACKAGE_TESTING_PACKAGES_PATH, "invalid_spl_file-ACD-1682.spl"), False),
    (os.path.join(APP_PACKAGE_TESTING_PACKAGES_PATH, "invalid_tar_file-ACD-1682.tgz"), False),
    (os.path.join(APP_PACKAGE_TESTING_PACKAGES_PATH, "invalid_tar_file-ACD-1682.tar.gz"), False),
    (os.path.join(APP_PACKAGE_TESTING_PACKAGES_PATH, "invalid_zip_file-ACD-1682.zip"), False),
    # Valid - these are all either FolderAppPackages or valid compressed files
    # that properly extract and contain no traversal attacks
    (os.path.join(APP_PACKAGE_TESTING_PACKAGES_PATH, ".is_a_hidden_directory_package-ACD-1362"), False),
    (os.path.join(APP_PACKAGE_TESTING_PACKAGES_PATH, ".is_a_hidden_spl_package-ACD-1362.spl"), False),
    (os.path.join(APP_PACKAGE_TESTING_PACKAGES_PATH, ".is_a_hidden_tar_gz_package-ACD-1362.tar.gz"), False),
    (os.path.join(APP_PACKAGE_TESTING_PACKAGES_PATH, ".is_a_hidden_tgz_package-ACD-1362.tgz"), False),
    (os.path.join(APP_PACKAGE_TESTING_PACKAGES_PATH, ".is_a_hidden_zip_package-ACD-1362.zip"), False),
    (os.path.join(APPINSPECT_TEST_PACKAGES_PATH, "good_app_conf"), False),
    (os.path.join(APP_PACKAGE_TESTING_PACKAGES_PATH, "good_app_conf.spl"), False),
    (os.path.join(APP_PACKAGE_TESTING_PACKAGES_PATH, "good_app_conf.tar.gz"), False),
    (os.path.join(APP_PACKAGE_TESTING_PACKAGES_PATH, "good_app_conf.tgz"), False),
    (os.path.join(APP_PACKAGE_TESTING_PACKAGES_PATH, "good_app_conf.zip"), False),
    (os.path.join(APP_PACKAGE_TESTING_PACKAGES_PATH, "extracts_to_file-ACD-1556.spl"), False),
    (os.path.join(APP_PACKAGE_TESTING_PACKAGES_PATH, "extracts_to_file-ACD-1556.tar.gz"), False),
    (os.path.join(APP_PACKAGE_TESTING_PACKAGES_PATH, "extracts_to_file-ACD-1556.tgz"), False),
    (os.path.join(APP_PACKAGE_TESTING_PACKAGES_PATH, "extracts_to_file-ACD-1556.zip"), False),
    (os.path.join(APP_PACKAGE_TESTING_PACKAGES_PATH, ".has_package_name_that_is_hidden_directory-ACD-1362"), False),
    (os.path.join(APP_PACKAGE_TESTING_PACKAGES_PATH, "has_package_name_that_is_hidden_directory-ACD-1362.tgz"), False),
    (os.path.join(APP_PACKAGE_TESTING_PACKAGES_PATH, "has_package_name_that_is_hidden_directory-ACD-1362.tar.gz"), False),
    (os.path.join(APP_PACKAGE_TESTING_PACKAGES_PATH, "has_package_name_that_is_hidden_directory-ACD-1362.spl"), False),
    (os.path.join(APP_PACKAGE_TESTING_PACKAGES_PATH, "has_package_name_that_is_hidden_directory-ACD-1362.zip"), False),
    (os.path.join(APP_PACKAGE_TESTING_PACKAGES_PATH, "has_macosx_directory-ACD-1362"), False),
    (os.path.join(APP_PACKAGE_TESTING_PACKAGES_PATH, "has_macosx_directory-ACD-1362.spl"), False),
    (os.path.join(APP_PACKAGE_TESTING_PACKAGES_PATH, "has_macosx_directory-ACD-1362.tar.gz"), False),
    (os.path.join(APP_PACKAGE_TESTING_PACKAGES_PATH, "has_macosx_directory-ACD-1362.tgz"), False),
    (os.path.join(APP_PACKAGE_TESTING_PACKAGES_PATH, "has_macosx_directory-ACD-1362.zip"), False),
    (os.path.join(APP_PACKAGE_TESTING_PACKAGES_PATH, "has_hidden_directory-ACD-1362"), False),
    (os.path.join(APP_PACKAGE_TESTING_PACKAGES_PATH, "has_hidden_directory-ACD-1362.spl"), False),
    (os.path.join(APP_PACKAGE_TESTING_PACKAGES_PATH, "has_hidden_directory-ACD-1362.tar.gz"), False),
    (os.path.join(APP_PACKAGE_TESTING_PACKAGES_PATH, "has_hidden_directory-ACD-1362.tgz"), False),
    (os.path.join(APP_PACKAGE_TESTING_PACKAGES_PATH, "has_hidden_directory-ACD-1362.zip"), False),
    (os.path.join(APP_PACKAGE_TESTING_PACKAGES_PATH, "has_missing_app_conf_file-ACD-1362"), False),
    (os.path.join(APP_PACKAGE_TESTING_PACKAGES_PATH, "has_missing_app_conf_file-ACD-1362.spl"), False),
    (os.path.join(APP_PACKAGE_TESTING_PACKAGES_PATH, "has_missing_app_conf_file-ACD-1362.tar.gz"), False),
    (os.path.join(APP_PACKAGE_TESTING_PACKAGES_PATH, "has_missing_app_conf_file-ACD-1362.tgz"), False),
    (os.path.join(APP_PACKAGE_TESTING_PACKAGES_PATH, "has_missing_app_conf_file-ACD-1362.zip"), False),
    (os.path.join(APP_PACKAGE_TESTING_PACKAGES_PATH, "has_nested_good_tgz_spl_zip_splunk_apps-ACD-1310"), False),
    (os.path.join(APP_PACKAGE_TESTING_PACKAGES_PATH, "has_nested_good_tgz_spl_zip_splunk_apps-ACD-1310.tgz"), False),
    (os.path.join(APPINSPECT_TEST_PACKAGES_PATH, "good_app_conf"), False),
    (os.path.join(APP_PACKAGE_TESTING_PACKAGES_PATH, "good_app_conf.spl"), False),
    (os.path.join(APP_PACKAGE_TESTING_PACKAGES_PATH, "good_app_conf.tar.gz"), False),
    (os.path.join(APP_PACKAGE_TESTING_PACKAGES_PATH, "good_app_conf.tgz"), False),
    (os.path.join(APP_PACKAGE_TESTING_PACKAGES_PATH, "good_app_conf.zip"), False),
    (os.path.join(APP_PACKAGE_TESTING_PACKAGES_PATH, "has_hidden_dependencies_directory-ACD-1556"), False),
    (os.path.join(APP_PACKAGE_TESTING_PACKAGES_PATH, "has_hidden_dependencies_directory-ACD-1556", "has_hidden_dependencies_directory-ACD-1556"), False),
    (os.path.join(APP_PACKAGE_TESTING_PACKAGES_PATH, "has_hidden_dependencies_directory-ACD-1556.spl"), False),
    (os.path.join(APP_PACKAGE_TESTING_PACKAGES_PATH, "has_hidden_dependencies_directory-ACD-1556.tar.gz"), False),
    (os.path.join(APP_PACKAGE_TESTING_PACKAGES_PATH, "has_hidden_dependencies_directory-ACD-1556.tgz"), False),
    (os.path.join(APP_PACKAGE_TESTING_PACKAGES_PATH, "has_hidden_dependencies_directory-ACD-1556.zip"), False),
]
# ==============================================================================
# does_traversal_attack_exist testing
# ==============================================================================
@pytest.mark.parametrize("test_package_path,expected_traversal_attack_exists", origin_artifact_traversal_attack_exists_test_parameters)
def test_app_package_does_traversal_attack_exist(test_package_path, expected_traversal_attack_exists):
    """Tests that the AppPackage class is correctly cleaning up all AppPackages
    including any extracted temp directories.
    """
    app_package_handler = splunk_appinspect.app_package_handler.AppPackageHandler(test_package_path)
    app_package_handler.cleanup()
    packages_to_test = app_package_handler.app_packages[:]
    if not app_package_handler.origin_package in packages_to_test:
        packages_to_test.append(app_package_handler.origin_package)
    for app_package in packages_to_test:
        if not isinstance(app_package, splunk_appinspect.app_package_handler.TarAppPackage):
            continue
        temporary_directory = tempfile.mkdtemp()
        try:
            traversal_attack_exists = False
            with tarfile.open(app_package.origin_path) as tar:
                traversal_attack_exists = splunk_appinspect.app_package_handler.TarAppPackage.does_traversal_attack_exist(
                    app_package.origin_path,
                    temporary_directory,
                    tar.getnames())
        except Exception as e:
            pass
        finally:
            shutil.rmtree(temporary_directory)
        assertion_output = ("TarAppPackage.does_traversal_attack_exist expected"
                            " `{}` received `{}`".format(
                            expected_traversal_attack_exists,
                            traversal_attack_exists))
        assert expected_traversal_attack_exists == traversal_attack_exists, assertion_output


# ==============================================================================
# origin_artifact_name testing
# ==============================================================================
origin_artifact_name_test_parameters = [
    # Invalid - Packages that start with a `.`
    (os.path.join(APP_PACKAGE_TESTING_PACKAGES_PATH, ".is_a_hidden_directory_package-ACD-1362"), ".is_a_hidden_directory_package-ACD-1362"),
    (os.path.join(APP_PACKAGE_TESTING_PACKAGES_PATH, ".is_a_hidden_spl_package-ACD-1362.spl"), ".is_a_hidden_spl_package-ACD-1362"),
    (os.path.join(APP_PACKAGE_TESTING_PACKAGES_PATH, ".is_a_hidden_tar_gz_package-ACD-1362.tar.gz"), ".is_a_hidden_tar_gz_package-ACD-1362"),
    (os.path.join(APP_PACKAGE_TESTING_PACKAGES_PATH, ".is_a_hidden_tgz_package-ACD-1362.tgz"), ".is_a_hidden_tgz_package-ACD-1362"),
    (os.path.join(APP_PACKAGE_TESTING_PACKAGES_PATH, ".is_a_hidden_zip_package-ACD-1362.zip"), ".is_a_hidden_zip_package-ACD-1362"),
    # Invalid - Has a package that when extracted starts with a `.`
    (os.path.join(APP_PACKAGE_TESTING_PACKAGES_PATH, ".has_package_name_that_is_hidden_directory-ACD-1362"), ".has_package_name_that_is_hidden_directory-ACD-1362"),
    (os.path.join(APP_PACKAGE_TESTING_PACKAGES_PATH, "has_package_name_that_is_hidden_directory-ACD-1362.tgz"), "has_package_name_that_is_hidden_directory-ACD-1362"),
    (os.path.join(APP_PACKAGE_TESTING_PACKAGES_PATH, "has_package_name_that_is_hidden_directory-ACD-1362.tar.gz"), "has_package_name_that_is_hidden_directory-ACD-1362"),
    (os.path.join(APP_PACKAGE_TESTING_PACKAGES_PATH, "has_package_name_that_is_hidden_directory-ACD-1362.spl"), "has_package_name_that_is_hidden_directory-ACD-1362"),
    (os.path.join(APP_PACKAGE_TESTING_PACKAGES_PATH, "has_package_name_that_is_hidden_directory-ACD-1362.zip"), "has_package_name_that_is_hidden_directory-ACD-1362"),
    # Invalid - Has a package that contains a __MACOSX file
    (os.path.join(APP_PACKAGE_TESTING_PACKAGES_PATH, "has_macosx_directory-ACD-1362"), "has_macosx_directory-ACD-1362"),
    (os.path.join(APP_PACKAGE_TESTING_PACKAGES_PATH, "has_macosx_directory-ACD-1362.spl"), "has_macosx_directory-ACD-1362"),
    (os.path.join(APP_PACKAGE_TESTING_PACKAGES_PATH, "has_macosx_directory-ACD-1362.tar.gz"), "has_macosx_directory-ACD-1362"),
    (os.path.join(APP_PACKAGE_TESTING_PACKAGES_PATH, "has_macosx_directory-ACD-1362.tgz"), "has_macosx_directory-ACD-1362"),
    (os.path.join(APP_PACKAGE_TESTING_PACKAGES_PATH, "has_macosx_directory-ACD-1362.zip"), "has_macosx_directory-ACD-1362"),
    # Invalid - Has a package that contains a hidden directory
    (os.path.join(APP_PACKAGE_TESTING_PACKAGES_PATH, "has_hidden_directory-ACD-1362"), "has_hidden_directory-ACD-1362"),
    (os.path.join(APP_PACKAGE_TESTING_PACKAGES_PATH, "has_hidden_directory-ACD-1362.spl"), "has_hidden_directory-ACD-1362"),
    (os.path.join(APP_PACKAGE_TESTING_PACKAGES_PATH, "has_hidden_directory-ACD-1362.tar.gz"), "has_hidden_directory-ACD-1362"),
    (os.path.join(APP_PACKAGE_TESTING_PACKAGES_PATH, "has_hidden_directory-ACD-1362.tgz"), "has_hidden_directory-ACD-1362"),
    (os.path.join(APP_PACKAGE_TESTING_PACKAGES_PATH, "has_hidden_directory-ACD-1362.zip"), "has_hidden_directory-ACD-1362"),
    # Invalid - Nested valid apps, but main structure is not considered valid
    (os.path.join(APP_PACKAGE_TESTING_PACKAGES_PATH, "has_nested_good_tgz_spl_zip_splunk_apps-ACD-1310"), "has_nested_good_tgz_spl_zip_splunk_apps-ACD-1310"),
    (os.path.join(APP_PACKAGE_TESTING_PACKAGES_PATH, "has_nested_good_tgz_spl_zip_splunk_apps-ACD-1310.tgz"), "has_nested_good_tgz_spl_zip_splunk_apps-ACD-1310"),
    # Invalid - Packages are 0 bytes
    (os.path.join(APP_PACKAGE_TESTING_PACKAGES_PATH, "invalid_spl_file-ACD-1682.spl"), "invalid_spl_file-ACD-1682"),
    (os.path.join(APP_PACKAGE_TESTING_PACKAGES_PATH, "invalid_tar_file-ACD-1682.tgz"), "invalid_tar_file-ACD-1682"),
    (os.path.join(APP_PACKAGE_TESTING_PACKAGES_PATH, "invalid_tar_file-ACD-1682.tar.gz"), "invalid_tar_file-ACD-1682"),
    (os.path.join(APP_PACKAGE_TESTING_PACKAGES_PATH, "invalid_zip_file-ACD-1682.zip"), "invalid_zip_file-ACD-1682"),
    # Invalid - Traversal attack attempts to extract to absolute path
    # /etc/passwd1 created using `tar -cPf foo.tar /etc/passwd1`
    (os.path.join(APP_PACKAGE_TESTING_PACKAGES_PATH, "traversal_attack_to_etc_passwd1.tgz"), "traversal_attack_to_etc_passwd1"),
    (os.path.join(APP_PACKAGE_TESTING_PACKAGES_PATH, "traversal_attack_to_etc_passwd1.tar.gz"), "traversal_attack_to_etc_passwd1"),
    # Invalid - Traversal attack attempts to extract to relative path
    # ../../badfile created using `tar -cPf foo.tar ../../badfile`
    (os.path.join(APP_PACKAGE_TESTING_PACKAGES_PATH, "traversal_attack_relative_path_two_levels_back.tgz"), "traversal_attack_relative_path_two_levels_back"),
    (os.path.join(APP_PACKAGE_TESTING_PACKAGES_PATH, "traversal_attack_relative_path_two_levels_back.tar.gz"), "traversal_attack_relative_path_two_levels_back"),
    # Valid
    (os.path.join(APPINSPECT_TEST_PACKAGES_PATH, "good_app_conf"), "good_app_conf"),
    (os.path.join(APP_PACKAGE_TESTING_PACKAGES_PATH, "good_app_conf.spl"), "good_app_conf"),
    (os.path.join(APP_PACKAGE_TESTING_PACKAGES_PATH, "good_app_conf.tar.gz"), "good_app_conf"),
    (os.path.join(APP_PACKAGE_TESTING_PACKAGES_PATH, "good_app_conf.tgz"), "good_app_conf"),
    (os.path.join(APP_PACKAGE_TESTING_PACKAGES_PATH, "good_app_conf.zip"), "good_app_conf"),
]


@pytest.mark.parametrize("test_package_path,expected_result", origin_artifact_name_test_parameters)
def test_origin_artifact_name(test_package_path, expected_result):
    """A test to confirm that the helper functions exposed for getting the name
    of the initial package provided is returning the correct name.
    """
    app_package = splunk_appinspect.app_package_handler.AppPackage.factory(test_package_path)
    origin_artifact_name = app_package.origin_artifact_name
    assertion_output = ("The package `{}` for the property"
                        " `origin_artifact_name `"
                        " expected the result `{}`, but received `{}`"
                        ).format(test_package_path,
                                 expected_result,
                                 origin_artifact_name)
    app_package.clean_up()
    assert origin_artifact_name == expected_result, assertion_output


# ==============================================================================
# working_artifact_name testing
# ==============================================================================
working_artifact_name_test_parameters = [
    # Invalid - Packages that start with a `.`
    (os.path.join(APP_PACKAGE_TESTING_PACKAGES_PATH, ".is_a_hidden_directory_package-ACD-1362"), ".is_a_hidden_directory_package-ACD-1362"),
    (os.path.join(APP_PACKAGE_TESTING_PACKAGES_PATH, ".is_a_hidden_spl_package-ACD-1362.spl"), "is_a_hidden_spl_package-ACD-1362"),
    (os.path.join(APP_PACKAGE_TESTING_PACKAGES_PATH, ".is_a_hidden_tar_gz_package-ACD-1362.tar.gz"), "is_a_hidden_tar_gz_package-ACD-1362"),
    (os.path.join(APP_PACKAGE_TESTING_PACKAGES_PATH, ".is_a_hidden_tgz_package-ACD-1362.tgz"), "is_a_hidden_tgz_package-ACD-1362"),
    (os.path.join(APP_PACKAGE_TESTING_PACKAGES_PATH, ".is_a_hidden_zip_package-ACD-1362.zip"), "is_a_hidden_zip_package-ACD-1362"),
    # Invalid - Has a package that when extracted starts with a `.`
    (os.path.join(APP_PACKAGE_TESTING_PACKAGES_PATH, ".has_package_name_that_is_hidden_directory-ACD-1362"), ".has_package_name_that_is_hidden_directory-ACD-1362"),
    (os.path.join(APP_PACKAGE_TESTING_PACKAGES_PATH, "has_package_name_that_is_hidden_directory-ACD-1362.tgz"), ".has_package_name_that_is_hidden_directory-ACD-1362"),
    (os.path.join(APP_PACKAGE_TESTING_PACKAGES_PATH, "has_package_name_that_is_hidden_directory-ACD-1362.tar.gz"), ".has_package_name_that_is_hidden_directory-ACD-1362"),
    (os.path.join(APP_PACKAGE_TESTING_PACKAGES_PATH, "has_package_name_that_is_hidden_directory-ACD-1362.spl"), ".has_package_name_that_is_hidden_directory-ACD-1362"),
    (os.path.join(APP_PACKAGE_TESTING_PACKAGES_PATH, "has_package_name_that_is_hidden_directory-ACD-1362.zip"), ".has_package_name_that_is_hidden_directory-ACD-1362"),
    # Invalid - Has a package that contains a __MACOSX file
    (os.path.join(APP_PACKAGE_TESTING_PACKAGES_PATH, "has_macosx_directory-ACD-1362"), "has_macosx_directory-ACD-1362"),
    (os.path.join(APP_PACKAGE_TESTING_PACKAGES_PATH, "has_macosx_directory-ACD-1362.spl"), "has_macosx_directory-ACD-1362"),
    (os.path.join(APP_PACKAGE_TESTING_PACKAGES_PATH, "has_macosx_directory-ACD-1362.tar.gz"), "has_macosx_directory-ACD-1362"),
    (os.path.join(APP_PACKAGE_TESTING_PACKAGES_PATH, "has_macosx_directory-ACD-1362.tgz"), "has_macosx_directory-ACD-1362"),
    (os.path.join(APP_PACKAGE_TESTING_PACKAGES_PATH, "has_macosx_directory-ACD-1362.zip"), "has_macosx_directory-ACD-1362"),
    # Invalid - Has a package that contains a hidden directory
    (os.path.join(APP_PACKAGE_TESTING_PACKAGES_PATH, "has_hidden_directory-ACD-1362"), "has_hidden_directory-ACD-1362"),
    (os.path.join(APP_PACKAGE_TESTING_PACKAGES_PATH, "has_hidden_directory-ACD-1362.spl"), "has_hidden_directory-ACD-1362"),
    (os.path.join(APP_PACKAGE_TESTING_PACKAGES_PATH, "has_hidden_directory-ACD-1362.tar.gz"), "has_hidden_directory-ACD-1362"),
    (os.path.join(APP_PACKAGE_TESTING_PACKAGES_PATH, "has_hidden_directory-ACD-1362.tgz"), "has_hidden_directory-ACD-1362"),
    (os.path.join(APP_PACKAGE_TESTING_PACKAGES_PATH, "has_hidden_directory-ACD-1362.zip"), "has_hidden_directory-ACD-1362"),
    # Invalid - Nested valid apps, but main structure is not considered valid
    (os.path.join(APP_PACKAGE_TESTING_PACKAGES_PATH, "has_nested_good_tgz_spl_zip_splunk_apps-ACD-1310"), "has_nested_good_tgz_spl_zip_splunk_apps-ACD-1310"),
    (os.path.join(APP_PACKAGE_TESTING_PACKAGES_PATH, "has_nested_good_tgz_spl_zip_splunk_apps-ACD-1310.tgz"), "has_nested_good_tgz_spl_zip_splunk_apps-ACD-1310"),
    # Invalid - Packages are 0 bytes
    (os.path.join(APP_PACKAGE_TESTING_PACKAGES_PATH, "invalid_spl_file-ACD-1682.spl"), "invalid_spl_file-ACD-1682"),
    (os.path.join(APP_PACKAGE_TESTING_PACKAGES_PATH, "invalid_tar_file-ACD-1682.tgz"), "invalid_tar_file-ACD-1682"),
    (os.path.join(APP_PACKAGE_TESTING_PACKAGES_PATH, "invalid_tar_file-ACD-1682.tar.gz"), "invalid_tar_file-ACD-1682"),
    (os.path.join(APP_PACKAGE_TESTING_PACKAGES_PATH, "invalid_zip_file-ACD-1682.zip"), "invalid_zip_file-ACD-1682"),
    # Invalid - Traversal attack attempts to extract to absolute path
    # /etc/passwd1 created using `tar -cPf foo.tar /etc/passwd1`
    (os.path.join(APP_PACKAGE_TESTING_PACKAGES_PATH, "traversal_attack_to_etc_passwd1.tgz"), "traversal_attack_to_etc_passwd1"),
    (os.path.join(APP_PACKAGE_TESTING_PACKAGES_PATH, "traversal_attack_to_etc_passwd1.tar.gz"), "traversal_attack_to_etc_passwd1"),
    # Invalid - Traversal attack attempts to extract to relative path
    # ../../badfile created using `tar -cPf foo.tar ../../badfile`
    (os.path.join(APP_PACKAGE_TESTING_PACKAGES_PATH, "traversal_attack_relative_path_two_levels_back.tgz"), "traversal_attack_relative_path_two_levels_back"),
    (os.path.join(APP_PACKAGE_TESTING_PACKAGES_PATH, "traversal_attack_relative_path_two_levels_back.tar.gz"), "traversal_attack_relative_path_two_levels_back"),
    # Valid
    (os.path.join(APPINSPECT_TEST_PACKAGES_PATH, "good_app_conf"), "good_app_conf"),
    (os.path.join(APP_PACKAGE_TESTING_PACKAGES_PATH, "good_app_conf.spl"), "good_app_conf"),
    (os.path.join(APP_PACKAGE_TESTING_PACKAGES_PATH, "good_app_conf.tar.gz"), "good_app_conf"),
    (os.path.join(APP_PACKAGE_TESTING_PACKAGES_PATH, "good_app_conf.tgz"), "good_app_conf"),
    (os.path.join(APP_PACKAGE_TESTING_PACKAGES_PATH, "good_app_conf.zip"), "good_app_conf"),
]


@pytest.mark.parametrize("test_package_path,expected_result", working_artifact_name_test_parameters)
def test_working_artifact_name(test_package_path, expected_result):
    """A test to confirm that the helper functions exposed for getting the name
    of the extracted package provided is returning the correct name.
    """
    app_package = splunk_appinspect.app_package_handler.AppPackage.factory(test_package_path)
    working_artifact_name = app_package.working_artifact_name
    assertion_output = ("The package `{}` for the property"
                        " `working_artifact_name `"
                        " expected the result `{}`, but received `{}`"
                        ).format(test_package_path,
                                 expected_result,
                                 working_artifact_name)
    app_package.clean_up()
    assert working_artifact_name == expected_result, assertion_output

directory_permission_test_parameters = [
    (os.path.join(APP_PACKAGE_TESTING_PACKAGES_PATH, "has_invalid_directory_with_wrong_permission_PBL-4786"), "", True),
    (os.path.join(APP_PACKAGE_TESTING_PACKAGES_PATH, "has_invalid_directory_with_wrong_permission_PBL-4786"),
     "default/data/models/", True),
]


@pytest.mark.skipif(os.name != "posix", reason="Only runs on Linux or OSX platform.")
@pytest.mark.parametrize("test_package_path,sub_directory,expected_result", directory_permission_test_parameters)
def test_app_contains_directory_with_incorrect_permission(test_package_path, sub_directory, expected_result):
    """A test to determine that the app directory contains invalid folders with incorrect permissions.
    Directories and sub directories must have have the owner's permissions set to r/w/x (700).
    set to r/w/x (700) for all directories.
    """

    invalid_directory = os.path.join(test_package_path, sub_directory)
    try:
        # chmod the directory owner permission
        os.chmod(invalid_directory, stat.S_IWUSR)

        app_package = splunk_appinspect.app_package_handler.AppPackage.factory(test_package_path)
        contain_invalid_directories = app_package.does_contain_invalid_directories()
        assertion_output = ("The package `{}` for the function"
                            " `does_contain_invalid_directories()`"
                            " expected the result `{}`, but received `{}`"
                            ).format(test_package_path,
                                     expected_result,
                                     contain_invalid_directories)
        app_package.clean_up()
    finally:
        # recover the owner permission
        os.chmod(invalid_directory, stat.S_IRWXU)
    assert contain_invalid_directories == expected_result, assertion_output


file_permission_test_parameters = [
    (os.path.join(APP_PACKAGE_TESTING_PACKAGES_PATH, "has_files_with_invalid_permissions-PBL-4787"),
     "", False),
    (os.path.join(APP_PACKAGE_TESTING_PACKAGES_PATH, "has_files_with_invalid_permissions-PBL-4787"),
     "invalid_file.txt", True),
    (os.path.join(APP_PACKAGE_TESTING_PACKAGES_PATH, "has_files_with_invalid_permissions-PBL-4787"),
     "folder_with_invalid_file/another_invalid_file.txt", True),
]


@pytest.mark.parametrize("test_package_path,filepath,expected_result", file_permission_test_parameters)
def test_app_contains_file_with_incorrect_permission(test_package_path, filepath, expected_result):
    """A test to determine that the app directory contains invalid files with incorrect permissions.
    Files must have have the owner's permissions set to r/w (600).
    """

    invalid_file = os.path.join(test_package_path, filepath)
    try:
        # chmod the file owner permission if marked as 'invalid_file.txt'
        if 'invalid_file.txt' in invalid_file:
            os.chmod(invalid_file, stat.S_IXUSR | stat.S_IRUSR)

        app_package = splunk_appinspect.app_package_handler.AppPackage.factory(test_package_path)
        contain_invalid_files = app_package.does_contain_invalid_files()
        assertion_output = ("The package `{}` for the function"
                            " `does_contain_invalid_files()`"
                            " expected the result `{}`, but received `{}`"
                            ).format(test_package_path,
                                     expected_result,
                                     contain_invalid_files)
        app_package.clean_up()
    finally:
        # recover the owner permission if marked as 'invalid_file.txt'
        if 'invalid_file.txt' in invalid_file:
            os.chmod(invalid_file, stat.S_IWUSR | stat.S_IRUSR | stat.S_IRGRP | stat.S_IROTH)
    assert contain_invalid_files == expected_result, assertion_output

origin_artifact_permission_test_parameters = [
    (os.path.join(APP_PACKAGE_TESTING_PACKAGES_PATH, "has_valid_read_permission-PBL-5212.spl"), True),
    (os.path.join(APP_PACKAGE_TESTING_PACKAGES_PATH, "has_missing_read_permission-PBL-5212"), False),
    (os.path.join(APP_PACKAGE_TESTING_PACKAGES_PATH, "has_missing_read_permission-PBL-5212.spl"), False),
    (os.path.join(APP_PACKAGE_TESTING_PACKAGES_PATH, "has_missing_read_permission-PBL-5212.tar.gz"), False),
    (os.path.join(APP_PACKAGE_TESTING_PACKAGES_PATH, "has_missing_read_permission-PBL-5212.tgz"), False),
    (os.path.join(APP_PACKAGE_TESTING_PACKAGES_PATH, "has_missing_read_permission-PBL-5212.zip"), False),
]


@pytest.mark.skipif(os.name != "posix", reason="Only runs on Linux or OSX platform.")
@pytest.mark.parametrize("test_package_path,expected_result", origin_artifact_permission_test_parameters)
def test_origin_artifact_requires_read_permission(test_package_path, expected_result):
    """A test to determine that the package will fail if it is missing owner read permission (400).
    """
    try:
        # chmod the package owner permission
        if 'has_missing_read_permission' in test_package_path:
            os.chmod(test_package_path, stat.S_IWUSR | stat.S_IRGRP | stat.S_IROTH)

        app_package = splunk_appinspect.app_package_handler.AppPackage.factory(test_package_path)
        contain_read_permission = app_package.does_origin_artifact_have_read_permission()
        assertion_output = ("The package `{}` for the function"
                            " `does_origin_artifact_have_read_permission()`"
                            " expected the result `{}`, but received `{}`"
                            ).format(test_package_path,
                                     expected_result,
                                     contain_read_permission)
        app_package.clean_up()
    finally:
        # recover the owner permission
        os.chmod(test_package_path, stat.S_IRUSR | stat.S_IWUSR | stat.S_IRGRP | stat.S_IROTH)
    assert contain_read_permission == expected_result, assertion_output