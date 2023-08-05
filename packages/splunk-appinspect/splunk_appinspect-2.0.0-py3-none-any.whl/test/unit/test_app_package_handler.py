"""A test module to help validate the AppPackageHandler class's features."""

# Python Standard Libraries
import os
import tempfile
import unittest
# Third-Party Libraries
import mock
import pytest
# Custom Libraries
from splunk_appinspect.app_package_handler import AppPackageHandler

APP_PACKAGES = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'packages', 'app_package_testing_packages')
PACKAGES = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'packages')

GOOD_ZIP = os.path.join(APP_PACKAGES, 'good_app_conf.zip')
GOOD_TGZ = os.path.join(APP_PACKAGES, 'good_app_conf.tgz')
GOOD_FDR = os.path.join(PACKAGES, 'good_app_conf')

# Each of these have three nested apps
NESTED_APPS_TGZ = os.path.join(APP_PACKAGES,
                               "has_nested_good_tgz_spl_zip_splunk_apps-ACD-1310.tgz")
NESTED_APPS_DIRECTORY = os.path.join(APP_PACKAGES,
                                     "has_nested_good_tgz_spl_zip_splunk_apps-ACD-1310")

# These are complicated nested slim dependencies. The most complex example
# (has_three_static_slim_dependencies_three_levels_deep-0.0.1.tar.gz) has a
# total of 8 app folders due to the odd convention that SLIM uses - it packages
# all of the unique sub-dependencies in the root .dependencies directory of the
# outermost app, we're not sure whether this is a bug or a feature but as a
# result the sub-depedencies are essentially packaged multiple times:
#
# has_three_static_slim_dependencies_three_levels_deep-0.0.1.tar.gz
#   * has_three_static_slim_dependencies_three_levels_deep/
#   - .dependencies/
#     - has_no_slim_dependencies.tgz
#       * has_no_slim_dependencies/
#     - has_one_static_slim_dependency-0.0.1.tar.gz
#       * has_one_static_slim_dependency
#       - .dependencies/
#         - has_no_slim_dependencies.tgz
#           * has_no_slim_dependencies/
#     - has_two_static_slim_dependencies_two_levels_deep-0.0.1.tar.gz
#       * has_two_static_slim_dependencies_two_levels_deep/
#       - .dependencies/
#         - has_no_slim_dependencies.tgz
#           * has_no_slim_dependencies
#         - has_one_static_slim_dependency-0.0.1.tar.gz
#           * has_one_static_slim_dependency/
#           - .dependencies/
#             - has_no_slim_dependencies.tgz
#               * has_no_slim_dependencies
SLIM_THREE_DEPENDENCIES_THREE_LEVELS_DEEP = os.path.join(APP_PACKAGES,
    "has_three_static_slim_dependencies_three_levels_deep-0.0.1.tar.gz")
SLIM_THREE_PLUS_ONE_DEPENDENCIES_THREE_LEVELS_DEEP = os.path.join(APP_PACKAGES,
    "has_three_valid_static_slim_dependencies_and_one_extra_tarball_in_dot_dependencies_dir-0.0.1.tar.gz")
SLIM_TWO_DEPENDENCIES_TWO_LEVELS_DEEP = os.path.join(APP_PACKAGES,
    "has_two_static_slim_dependencies_two_levels_deep-0.0.1.tar.gz")
SLIM_TWO_DEPENDENCIES_ONE_LEVEL_DEEP = os.path.join(APP_PACKAGES,
    "has_two_static_slim_dependencies_one_level_deep-0.0.1.tar.gz")
HAS_HIDDEN_DEPENDENCIES_DIRECTORY = os.path.join(APP_PACKAGES,
    "has_hidden_dependencies_directory-ACD-1556.tar.gz")
SLIM_ONE_DEPENDENCY = os.path.join(APP_PACKAGES,
    "has_one_static_slim_dependency-0.0.1.tar.gz")
HAS_NON_APP_FILE_IN_DEPENDENCIES = os.path.join(APP_PACKAGES,
    "has_dependencies_dir_with_non_app_dependency_file")
HAS_NON_APP_FOLDER_IN_DEPENDENCIES = os.path.join(APP_PACKAGES,
    "has_dependencies_dir_with_non_app_dependency_folder")


class AppPackageHandlerTest(unittest.TestCase):

    def setUp(self):
        super(AppPackageHandlerTest, self).setUp()

    def test_app_pkg_handler_instance(self):
        """Test a AppPackageHandler instance"""
        handler = AppPackageHandler(GOOD_TGZ)

        self.assertIsNotNone(handler)
        assert isinstance(handler, AppPackageHandler)
        assert handler.generate_package_hash_from_dir() != 'N/A'
        assert handler.file_hash != 'N/A'

        handler = AppPackageHandler(GOOD_FDR)

        self.assertIsNotNone(handler)
        assert isinstance(handler, AppPackageHandler)
        assert handler.generate_package_hash_from_dir() != 'N/A'
        # for FDR, the file hash should be not available
        assert handler.file_hash == 'N/A'

    # TODO(dnguyen): need to write more tests.  Will release this as hotfix as
    #   QA has already tested.


# Testing lists
good_packages = [GOOD_ZIP, GOOD_TGZ, GOOD_FDR]
nested_app_packages = [NESTED_APPS_TGZ, NESTED_APPS_DIRECTORY]


app_package_handler_general_apps_with_total_app_count = [
    (GOOD_ZIP, 1),
    (GOOD_TGZ, 1),
    (GOOD_FDR, 1),
    (NESTED_APPS_TGZ, 3),
    (NESTED_APPS_DIRECTORY, 3),
    (SLIM_THREE_DEPENDENCIES_THREE_LEVELS_DEEP, 8),
    (SLIM_THREE_PLUS_ONE_DEPENDENCIES_THREE_LEVELS_DEEP, 9),
    (SLIM_TWO_DEPENDENCIES_TWO_LEVELS_DEEP, 4),
    (SLIM_TWO_DEPENDENCIES_ONE_LEVEL_DEEP, 3),
    (HAS_HIDDEN_DEPENDENCIES_DIRECTORY, 2),
    (SLIM_ONE_DEPENDENCY, 2),
    (HAS_NON_APP_FILE_IN_DEPENDENCIES, 2),
    (HAS_NON_APP_FOLDER_IN_DEPENDENCIES, 2),
]

app_package_handler_main_app_package_location_tests = [
    (GOOD_ZIP, GOOD_ZIP),
    (GOOD_TGZ, GOOD_TGZ),
    (GOOD_FDR, GOOD_FDR),
    # There is no way to test that the main package is correctly selected in a
    # nested tgz app as it gets extracted to a temporary directory and will not
    # match with the file path that it was pulled from
    (NESTED_APPS_DIRECTORY, [
            os.path.join(APP_PACKAGES, "has_nested_good_tgz_spl_zip_splunk_apps-ACD-1310", "good_app_conf.spl"),
            os.path.join(APP_PACKAGES, "has_nested_good_tgz_spl_zip_splunk_apps-ACD-1310", "good_app_conf.tgz"),
            os.path.join(APP_PACKAGES, "has_nested_good_tgz_spl_zip_splunk_apps-ACD-1310", "good_app_conf.zip")
        ]),
]


@pytest.mark.parametrize("test_package_path,expected_app_packages_count", app_package_handler_general_apps_with_total_app_count)
def test_app_package_handler_has_correct_app_packages_count(test_package_path, expected_app_packages_count):
    """Tests that the AppPackageHandler class is correctly identifying ALL
    Splunk Apps.
    """
    app_package_handler = AppPackageHandler(test_package_path)
    try:
        assert len(app_package_handler.app_packages) == expected_app_packages_count
        assert app_package_handler.generate_package_hash_from_dir() != 'N/A'
    finally:
        app_package_handler.cleanup()


@pytest.mark.parametrize("test_package_path,expected_main_package_path", app_package_handler_main_app_package_location_tests)
def test_app_package_handler_returns_correct_main_package(test_package_path, expected_main_package_path):
    """Tests that the AppPackageHandler class is correctly identifying the main
    Splunk App that is provided.
    """
    app_package_handler = AppPackageHandler(test_package_path)
    try:
        assert app_package_handler.main_app_package is not None
        # nested apps
        if isinstance(expected_main_package_path, list):
            assert app_package_handler.main_app_package.origin_path in expected_main_package_path
        else:
            assert app_package_handler.main_app_package.origin_path == expected_main_package_path
    finally:
        app_package_handler.cleanup()


@pytest.mark.parametrize("test_package_path,expected_app_packages_count", app_package_handler_general_apps_with_total_app_count)
def test_origin_package_is_cleaned_up_if_exception_during_init(test_package_path, expected_app_packages_count):
    """Tests that AppPackageHandler.__init__() cleans up temp directories for
    case where Exception is raised during creation.
    """
    tmp_directories_created = []
    unpatched_mkdtemp = tempfile.mkdtemp

    def _mkdtemp_tracker(suffix='', prefix='tmp', _dir=None):
        """Override this method to keep track of any temp directories created
        using tempfile.mkdtemp"""
        temp_dir = unpatched_mkdtemp(suffix, prefix, _dir)
        tmp_directories_created.append(temp_dir)
        return temp_dir

    def _raises_exception(self):
        raise Exception()
    try:
        app_package = None
        with mock.patch.object(tempfile, "mkdtemp", new=_mkdtemp_tracker):
            with mock.patch.object(AppPackageHandler,
                                   "_gather_package_dependencies",
                                   new=_raises_exception):
                app_package_handler = AppPackageHandler(test_package_path)
    finally:
        app_package_handler.cleanup()
    for temp_dir in tmp_directories_created:
        temp_directory_exists = os.path.exists(temp_dir)
        assertion_output = ("Created temp directory not removed from"
                            " package for test_package_path: `{}`"
                            .format(test_package_path))
        assert not temp_directory_exists, assertion_output


if __name__ == '__main__':
    unittest.main()
