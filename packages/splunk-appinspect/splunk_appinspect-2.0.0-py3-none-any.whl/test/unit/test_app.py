"""Module for testing the Splunk AppInspect App object."""

# Python Standard Libraries
import os
# Third-Party Libraries
import pytest
# Custom Libraries
import splunk_appinspect
from six import iteritems


APPINSPECT_TEST_PATH = os.path.dirname(os.path.abspath(__file__))
APPINSPECT_TEST_PACKAGES_PATH = os.path.join(APPINSPECT_TEST_PATH, "packages")
APP_PACKAGE_TESTING_PACKAGES_PATH = os.path.join(APPINSPECT_TEST_PACKAGES_PATH, "app_package_testing_packages")

app_package_name_test_parameters = [
    (os.path.join(APPINSPECT_TEST_PACKAGES_PATH, "good_app_conf"), "good_app_conf"),
    (os.path.join(APP_PACKAGE_TESTING_PACKAGES_PATH, "good_app_conf.spl"), "good_app_conf"),
    (os.path.join(APP_PACKAGE_TESTING_PACKAGES_PATH, "good_app_conf.tgz"), "good_app_conf"),
    (os.path.join(APP_PACKAGE_TESTING_PACKAGES_PATH, "good_app_conf.tar.gz"), "good_app_conf"),
    (os.path.join(APP_PACKAGE_TESTING_PACKAGES_PATH, "good_app_conf.zip"), "good_app_conf"),
    (os.path.join(APP_PACKAGE_TESTING_PACKAGES_PATH, "has_nested_good_tgz_spl_zip_splunk_apps-ACD-1310"), "has_nested_good_tgz_spl_zip_splunk_apps-ACD-1310"),
    (os.path.join(APP_PACKAGE_TESTING_PACKAGES_PATH, "has_nested_good_tgz_spl_zip_splunk_apps-ACD-1310.tgz"), "has_nested_good_tgz_spl_zip_splunk_apps-ACD-1310"),
]

general_app_package_test_parameters = [
    (os.path.join(APPINSPECT_TEST_PACKAGES_PATH, "good_app_conf")),
    (os.path.join(APP_PACKAGE_TESTING_PACKAGES_PATH, "good_app_conf.spl")),
    (os.path.join(APP_PACKAGE_TESTING_PACKAGES_PATH, "good_app_conf.tgz")),
    (os.path.join(APP_PACKAGE_TESTING_PACKAGES_PATH, "good_app_conf.tar.gz")),
    (os.path.join(APP_PACKAGE_TESTING_PACKAGES_PATH, "good_app_conf.zip")),
    (os.path.join(APP_PACKAGE_TESTING_PACKAGES_PATH, "has_nested_good_tgz_spl_zip_splunk_apps-ACD-1310")),
    (os.path.join(APP_PACKAGE_TESTING_PACKAGES_PATH, "has_nested_good_tgz_spl_zip_splunk_apps-ACD-1310.tgz")),
    (os.path.join(APP_PACKAGE_TESTING_PACKAGES_PATH, "has_hidden_dependencies_directory-ACD-1556")),
    (os.path.join(APP_PACKAGE_TESTING_PACKAGES_PATH, "has_hidden_dependencies_directory-ACD-1556.spl")),
    (os.path.join(APP_PACKAGE_TESTING_PACKAGES_PATH, "has_hidden_dependencies_directory-ACD-1556.tar.gz")),
    (os.path.join(APP_PACKAGE_TESTING_PACKAGES_PATH, "has_hidden_dependencies_directory-ACD-1556.tgz")),
    (os.path.join(APP_PACKAGE_TESTING_PACKAGES_PATH, "has_hidden_dependencies_directory-ACD-1556.zip")),
    (os.path.join(APP_PACKAGE_TESTING_PACKAGES_PATH, "ta_aob_sample_2_2_0-1.0.0.spl")),
]

missing_default_app_conf = [
    (os.path.join(APP_PACKAGE_TESTING_PACKAGES_PATH, "has_missing_app_conf_file-ACD-1362")),
    (os.path.join(APP_PACKAGE_TESTING_PACKAGES_PATH, "has_missing_app_conf_file-ACD-1362.spl")),
    (os.path.join(APP_PACKAGE_TESTING_PACKAGES_PATH, "has_missing_app_conf_file-ACD-1362.tgz")),
    (os.path.join(APP_PACKAGE_TESTING_PACKAGES_PATH, "has_missing_app_conf_file-ACD-1362.tar.gz")),
    (os.path.join(APP_PACKAGE_TESTING_PACKAGES_PATH, "has_missing_app_conf_file-ACD-1362.zip")),
]

# ==============================================================================
# App Initialization Testing Using Positional Parameter `location`
# ==============================================================================
# Test that the properties of the App object is correctly initialized The
# `package_handler` keyword parameter takes precedence over the `location`
# parameter


@pytest.mark.parametrize("test_package_path", general_app_package_test_parameters)
def test_app_dir_initialization_using_positional_parameter(test_package_path):
    """"Tests initialization value for app.app_dir matches package handler when
    App(package_path) initialization is used.
    """
    app = splunk_appinspect.App(test_package_path)
    app_dir = app.app_dir
    assertion_output = ("`test_app_dir_initialization_using_positional_parameter`"
                        " expected: `{}`"
                        " received: `{}`").format(app.package.working_app_path,
                                                  app_dir)
    assert app_dir == app.package.working_app_path, assertion_output


@pytest.mark.parametrize("test_package_path", general_app_package_test_parameters)
def test_dependencies_directory_path_initialization_using_positional_parameter(test_package_path):
    """"Tests initialization value for app.dependencies_directory_path matches
    package handler when App(package_path) initialization is used.
    """
    app = splunk_appinspect.App(test_package_path)
    dependencies_directory_path = os.path.abspath(os.path.join(app.app_dir,
        app.dependencies_directory_path))
    expected_location = os.path.abspath(os.path.join(
        app.package.working_app_path, os.path.pardir,
        app.package.DEPENDENCIES_LOCATION))
    assertion_output = ("`test_dependencies_directory_path_initialization_using_positional_parameter`"
                        " expected: `{}`"
                        " received: `{}`").format(expected_location,
                                                  dependencies_directory_path)
    assert expected_location == dependencies_directory_path, assertion_output


@pytest.mark.parametrize("test_package_path,expected_app_name", app_package_name_test_parameters)
def test_name_initialization_using_positional_parameter(test_package_path, expected_app_name):
    """Tests initialization for app.name using when App(package_path)
    initialization.
    """
    app = splunk_appinspect.App(test_package_path)
    app_name = app.name
    assertion_output = ("`test_app_dir_initialization_using_positional_parameter`"
                        " expected: `{}`"
                        " received: `{}`").format(expected_app_name,
                                                  app_name)
    assert app_name == expected_app_name, assertion_output


@pytest.mark.parametrize("test_package_path", general_app_package_test_parameters)
def test_package_initialization_using_positional_parameter(test_package_path):
    """Tests initialization value for app.package is an instance of AppPackage.
    """
    app = splunk_appinspect.App(test_package_path)
    # Identity confirmation that the correct property is referenced
    assert isinstance(app.package, splunk_appinspect.app_package_handler.AppPackage)


# ==============================================================================
# App Initialization Testing Using Positional Parameter `package`
# ==============================================================================
# Test that the properties of the App object is correctly initialized The
# `package_handler` keyword parameter takes precedence over the `location`
# parameter


@pytest.mark.parametrize("test_package_path", general_app_package_test_parameters)
def test_app_package_initialization_using_package_keyword_parameter(test_package_path):
    """"Tests initialization value for app.package matches package input when
    App(package=package) initialization is used.
    """
    package = splunk_appinspect.app_package_handler.AppPackage.factory(test_package_path)
    app = splunk_appinspect.App(package=package)
    app_package = app.package
    assertion_output = ("`test_app_package_initialization_using_package_keyword_parameter`"
                        " expected: `{}`"
                        " received: `{}`").format(package,
                                                  app_package)
    assert package == app_package, assertion_output


@pytest.mark.parametrize("test_package_path", general_app_package_test_parameters)
def test_app_dir_initialization_using_package_keyword_parameter(test_package_path):
    """"Tests initialization value for app.app_dir matches package handler when
    App(package=package) initialization is used.
    """
    package = splunk_appinspect.app_package_handler.AppPackage.factory(test_package_path)
    app = splunk_appinspect.App(package=package)
    app_dir = app.app_dir
    assertion_output = ("`test_app_dir_initialization_using_package_keyword_parameter`"
                        " expected: `{}`"
                        " received: `{}`").format(package.working_app_path,
                                                  app_dir)
    assert app_dir == app.package.working_app_path, assertion_output


@pytest.mark.parametrize("test_package_path", general_app_package_test_parameters)
def test_dependencies_directory_path_initialization_using_package_keyword_parameter(test_package_path):
    """"Tests initialization value for app.dependencies_directory_path matches
    package handler when App(package=package) initialization is used.
    """
    package = splunk_appinspect.app_package_handler.AppPackage.factory(test_package_path)
    app = splunk_appinspect.App(package=package)
    dependencies_directory_path = os.path.abspath(os.path.join(app.app_dir,
        app.dependencies_directory_path))
    expected_location = os.path.abspath(os.path.join(
        app.package.working_app_path, os.path.pardir,
        app.package.DEPENDENCIES_LOCATION))
    assertion_output = ("`test_dependencies_directory_path_initialization_using_package_keyword_parameter`"
                        " expected: `{}`"
                        " received: `{}`").format(expected_location,
                                                  dependencies_directory_path)
    assert expected_location == dependencies_directory_path, assertion_output

@pytest.mark.parametrize("test_package_path,expected_app_name", app_package_name_test_parameters)
def test_name_initialization_using_package_keyword_parameter(test_package_path, expected_app_name):
    """Tests initialization for app.name using when App(package=package)
    initialization.
    """
    package = splunk_appinspect.app_package_handler.AppPackage.factory(test_package_path)
    app = splunk_appinspect.App(package=package)
    app_name = app.name
    assertion_output = ("`test_name_initialization_using_package_keyword_parameter`"
                        " expected: `{}`"
                        " received: `{}`").format(expected_app_name,
                                                  app_name)
    assert app_name == expected_app_name, assertion_output


@pytest.mark.parametrize("test_package_path", general_app_package_test_parameters)
def test_package_initialization_using_package_keyword_parameter(test_package_path):
    """Tests initialization value for app.package is an instance of AppPackage.
    """
    package = splunk_appinspect.app_package_handler.AppPackage.factory(test_package_path)
    app = splunk_appinspect.App(package=package)
    # Identity confirmation that the correct property is referenced
    assert isinstance(app.package, splunk_appinspect.app_package_handler.AppPackage)


# ==============================================================================
# App Initialization Testing No Positional Parameters
# ==============================================================================
# Test that ValueError is raised when neither `location` nor `package`
# parameters are input.


def test_app_initialization_with_no_arguments():
    """"Tests initialization ValueError raised when App() initialization is
    used.
    """
    with pytest.raises(ValueError):
        app = splunk_appinspect.App()
    with pytest.raises(ValueError):
        app = splunk_appinspect.App(location=None)
    with pytest.raises(ValueError):
        app = splunk_appinspect.App(package=None)
    with pytest.raises(ValueError):
        app = splunk_appinspect.App(location=None, package=None)


# -------------------
# App Info Object
# -------------------
@pytest.mark.parametrize("test_package_path", missing_default_app_conf)
def test_app_info_missing_default_app_conf(test_package_path):
    """Test that the App.app_info method's returned dictionary has the correct
    properties, and those properties are correctly strings.
    """
    app = splunk_appinspect.App(test_package_path)
    app_info = app.app_info()

    assert app_info is not None
    assert isinstance(app_info, dict)
    assert app_info['author'] == "[MISSING `default/app.conf`]"
    assert app_info['description'] == "[MISSING `default/app.conf`]"
    assert app_info['version'] == "[MISSING `default/app.conf`]"
    assert app_info['label'] == "[MISSING `default/app.conf`]"
    assert app_info['name'] == "has_missing_app_conf_file-ACD-1362"


def test_app_info_default_app_conf_missing_launcher_stanza():
    """Test that the App.app_info method's returned dictionary has the correct
    properties, and those properties are strings when the `Launcher` stanza is
    missing.
    """
    app_path = os.path.join(APPINSPECT_TEST_PACKAGES_PATH,
                            "has_app_conf_with_empty_package_stanza-ACD-1061")
    app = splunk_appinspect.App(app_path)
    app_info = app.app_info()

    assert app_info is not None
    assert isinstance(app_info, dict)
    assert app_info['author'] == "[MISSING `default/app.conf` stanza `launcher`]"
    assert app_info['description'] == "[MISSING `default/app.conf` stanza `launcher`]"
    assert app_info['version'] == "[MISSING `default/app.conf` stanza `launcher`]"


def test_app_info_default_app_conf_missing_ui_stanza():
    """Test that the App.app_info method's returned dictionary has the correct
    properties, and those properties are strings when the `UI` stanza is
    missing.
    """
    app_path = os.path.join(APPINSPECT_TEST_PACKAGES_PATH,
                            "has_app_conf_with_empty_package_stanza-ACD-1061")
    app = splunk_appinspect.App(app_path)
    app_info = app.app_info()

    assert app_info is not None
    assert isinstance(app_info, dict)
    assert app_info['name'] == "has_app_conf_with_empty_package_stanza-ACD-1061"
    assert app_info['label'] == "[MISSING `default/app.conf` stanza `ui`]"


# -------------------
# App.get_config_file_paths
# -------------------
def test_app_get_config_file_paths():
    """
    Test whether get_config_file_paths method can return correctly
    """
    app_path = os.path.join(APPINSPECT_TEST_PACKAGES_PATH, "has_local_and_default_files-ACD-724")
    app = splunk_appinspect.App(app_path)

    app_conf_file_paths = app.get_config_file_paths('app.conf')
    assert app_conf_file_paths is not None
    assert isinstance(app_conf_file_paths, dict)
    assert 'local' in app_conf_file_paths
    assert 'default' in app_conf_file_paths

    props_conf_file_paths = app.get_config_file_paths('props.conf')
    assert props_conf_file_paths is not None
    assert isinstance(props_conf_file_paths, dict)
    assert 'local' in props_conf_file_paths
    assert 'default' not in props_conf_file_paths

# TODO (logan): Add unit tests for missing specific properties

# ==============================================================================
# App.name
# ==============================================================================
app_name_test_parameters = [
    # Should match the extracted directory name
    (os.path.join(APPINSPECT_TEST_PACKAGES_PATH, "good_app_conf"), "good_app_conf"),
    (os.path.join(APP_PACKAGE_TESTING_PACKAGES_PATH, "good_app_conf.spl"), "good_app_conf"),
    (os.path.join(APP_PACKAGE_TESTING_PACKAGES_PATH, "good_app_conf.tgz"), "good_app_conf"),
    (os.path.join(APP_PACKAGE_TESTING_PACKAGES_PATH, "good_app_conf.tar.gz"), "good_app_conf"),
    (os.path.join(APP_PACKAGE_TESTING_PACKAGES_PATH, "good_app_conf.zip"), "good_app_conf"),
    (os.path.join(APP_PACKAGE_TESTING_PACKAGES_PATH, "has_nested_good_tgz_spl_zip_splunk_apps-ACD-1310"), "has_nested_good_tgz_spl_zip_splunk_apps-ACD-1310"),
    (os.path.join(APP_PACKAGE_TESTING_PACKAGES_PATH, "has_nested_good_tgz_spl_zip_splunk_apps-ACD-1310.tgz"), "has_nested_good_tgz_spl_zip_splunk_apps-ACD-1310"),
    # Invalid - Has missing app.conf should still have a reliable name detection though
    (os.path.join(APP_PACKAGE_TESTING_PACKAGES_PATH, "has_missing_app_conf_file-ACD-1362"), "has_missing_app_conf_file-ACD-1362"),
    (os.path.join(APP_PACKAGE_TESTING_PACKAGES_PATH, "has_missing_app_conf_file-ACD-1362.spl"), "has_missing_app_conf_file-ACD-1362"),
    (os.path.join(APP_PACKAGE_TESTING_PACKAGES_PATH, "has_missing_app_conf_file-ACD-1362.tgz"), "has_missing_app_conf_file-ACD-1362"),
    (os.path.join(APP_PACKAGE_TESTING_PACKAGES_PATH, "has_missing_app_conf_file-ACD-1362.tar.gz"), "has_missing_app_conf_file-ACD-1362"),
    (os.path.join(APP_PACKAGE_TESTING_PACKAGES_PATH, "has_missing_app_conf_file-ACD-1362.zip"), "has_missing_app_conf_file-ACD-1362"),
    # Invalid - Packages are 0 bytes
    (os.path.join(APP_PACKAGE_TESTING_PACKAGES_PATH, "invalid_spl_file-ACD-1682.spl"), "invalid_spl_file-ACD-1682"),
    (os.path.join(APP_PACKAGE_TESTING_PACKAGES_PATH, "invalid_tar_file-ACD-1682.tgz"), "invalid_tar_file-ACD-1682"),
    (os.path.join(APP_PACKAGE_TESTING_PACKAGES_PATH, "invalid_tar_file-ACD-1682.tar.gz"), "invalid_tar_file-ACD-1682"),
    (os.path.join(APP_PACKAGE_TESTING_PACKAGES_PATH, "invalid_zip_file-ACD-1682.zip"), "invalid_zip_file-ACD-1682"),
]


@pytest.mark.parametrize("test_package_path,expected_result", app_name_test_parameters)
def test_app_name(test_package_path, expected_result):
    """Test that the App.name method's returns the correctly formatted
    name derived from the AppPackage
    """
    app = splunk_appinspect.App(test_package_path)
    app_name = app.name

    assert app_name is not None
    assert isinstance(app_name, str)
    assert app_name == expected_result


# Testing for static slim dependencies

# Parameters:
#   test_package_path (String): path to app package artifact to test
#       static_dependencies_definitions (Dict of arrays of Dicts): Dict where
#       keys are origin package filenames and values are arrays of static
#       dependencies represented by Dicts

static_slim_dependencies_test_parameters = [
    # These have no static dependencies
    (os.path.join(APPINSPECT_TEST_PACKAGES_PATH, "good_app_conf"), {"good_app_conf":[]}),
    (os.path.join(APP_PACKAGE_TESTING_PACKAGES_PATH, "good_app_conf.spl"), {"good_app_conf.spl":[]}),
    (os.path.join(APP_PACKAGE_TESTING_PACKAGES_PATH, "good_app_conf.tgz"), {"good_app_conf.tgz":[]}),
    (os.path.join(APP_PACKAGE_TESTING_PACKAGES_PATH, "good_app_conf.tar.gz"), {"good_app_conf.tar.gz":[]}),
    (os.path.join(APP_PACKAGE_TESTING_PACKAGES_PATH, "good_app_conf.zip"), {"good_app_conf.zip":[]}),
    (os.path.join(APP_PACKAGE_TESTING_PACKAGES_PATH, "has_nested_good_tgz_spl_zip_splunk_apps-ACD-1310"),
        {
            "good_app_conf.spl": [],
            "good_app_conf.tgz": [],
            "good_app_conf.zip": []
        }),
    (os.path.join(APP_PACKAGE_TESTING_PACKAGES_PATH, "has_nested_good_tgz_spl_zip_splunk_apps-ACD-1310.tgz"),
        {
            "good_app_conf.spl": [],
            "good_app_conf.tgz": [],
            "good_app_conf.zip": []
        }),
    (os.path.join(APP_PACKAGE_TESTING_PACKAGES_PATH, "has_missing_app_conf_file-ACD-1362"), {"has_missing_app_conf_file-ACD-1362":[]}),
    (os.path.join(APP_PACKAGE_TESTING_PACKAGES_PATH, "has_missing_app_conf_file-ACD-1362.spl"), {"has_missing_app_conf_file-ACD-1362.spl":[]}),
    (os.path.join(APP_PACKAGE_TESTING_PACKAGES_PATH, "has_missing_app_conf_file-ACD-1362.tgz"), {"has_missing_app_conf_file-ACD-1362.tgz":[]}),
    (os.path.join(APP_PACKAGE_TESTING_PACKAGES_PATH, "has_missing_app_conf_file-ACD-1362.tar.gz"), {"has_missing_app_conf_file-ACD-1362.tar.gz":[]}),
    (os.path.join(APP_PACKAGE_TESTING_PACKAGES_PATH, "has_missing_app_conf_file-ACD-1362.zip"), {"has_missing_app_conf_file-ACD-1362.zip":[]}),
    (os.path.join(APP_PACKAGE_TESTING_PACKAGES_PATH, "invalid_spl_file-ACD-1682.spl"), {"invalid_spl_file-ACD-1682.spl":[]}),
    (os.path.join(APP_PACKAGE_TESTING_PACKAGES_PATH, "invalid_tar_file-ACD-1682.tgz"), {"invalid_tar_file-ACD-1682.tgz":[]}),
    (os.path.join(APP_PACKAGE_TESTING_PACKAGES_PATH, "invalid_tar_file-ACD-1682.tar.gz"), {"invalid_tar_file-ACD-1682.tar.gz":[]}),
    (os.path.join(APP_PACKAGE_TESTING_PACKAGES_PATH, "invalid_zip_file-ACD-1682.zip"), {"invalid_zip_file-ACD-1682.zip":[]}),
    # These have a dependencies directory but the dependencies are rejected
    # because the package is invalid for one reason or another
    (os.path.join(APP_PACKAGE_TESTING_PACKAGES_PATH, "has_dependencies_dir_but_no_app_manifest"),
        {
            "has_dependencies_dir_but_no_app_manifest":
            [
                {
                    "good_app_conf-0.0.1.tar.gz": []
                }
            ]
        }),
    (os.path.join(APP_PACKAGE_TESTING_PACKAGES_PATH, "has_dependencies_dir_with_multiple_apps"),
        {
            "good_app_conf": [],
            "has_no_slim_dependencies": []
        }),
    # These have valid static dependencies
    (os.path.join(APP_PACKAGE_TESTING_PACKAGES_PATH, "has_dependencies_dir_with_non_app_dependency_file"),
        {
            "has_dependencies_dir_with_non_app_dependency_file":
            [
                {
                    "good_app_conf-0.0.1.tar.gz": []
                }
            ]
        }),
    (os.path.join(APP_PACKAGE_TESTING_PACKAGES_PATH, "has_dependencies_dir_with_non_app_dependency_folder"),
        {
            "has_dependencies_dir_with_non_app_dependency_folder":
            [
                {
                    "good_app_conf-0.0.1.tar.gz": []
                }
            ]
        }),
    (os.path.join(APP_PACKAGE_TESTING_PACKAGES_PATH, "has_one_static_slim_dependency-0.0.1.tar.gz"),
        {
            "has_one_static_slim_dependency-0.0.1.tar.gz":
            [
                {
                    "has_no_slim_dependencies.tgz": []
                }
            ]
        }),
    (os.path.join(APP_PACKAGE_TESTING_PACKAGES_PATH, "has_three_static_slim_dependencies_three_levels_deep-0.0.1.tar.gz"),
        {
            "has_three_static_slim_dependencies_three_levels_deep-0.0.1.tar.gz":
            [
                {
                    "has_no_slim_dependencies.tgz": []
                },
                {
                    "has_one_static_slim_dependency-0.0.1.tar.gz":
                    [
                        {
                            "has_no_slim_dependencies.tgz": []
                        }
                    ]
                },
                {
                    "has_two_static_slim_dependencies_two_levels_deep-0.0.1.tar.gz":
                    [
                        {
                            "has_no_slim_dependencies.tgz": []
                        },
                        {
                            "has_one_static_slim_dependency-0.0.1.tar.gz":
                            [
                                {
                                    "has_no_slim_dependencies.tgz": []
                                }
                            ]
                        }
                    ]
                }
            ]
        }),
    (os.path.join(APP_PACKAGE_TESTING_PACKAGES_PATH, "has_three_valid_static_slim_dependencies_and_one_extra_tarball_in_dot_dependencies_dir-0.0.1.tar.gz"),
        {
            "has_three_valid_static_slim_dependencies_and_one_extra_tarball_in_dot_dependencies_dir-0.0.1.tar.gz":
            [

                {
                    "good_app_conf-0.0.1.tar.gz": []
                },
                {
                    "has_no_slim_dependencies.tgz": []
                },
                {
                    "has_one_static_slim_dependency-0.0.1.tar.gz":
                    [
                        {
                            "has_no_slim_dependencies.tgz": []
                        }
                    ]
                },
                {
                    "has_two_static_slim_dependencies_two_levels_deep-0.0.1.tar.gz":
                    [
                        {
                            "has_no_slim_dependencies.tgz": []
                        },
                        {
                            "has_one_static_slim_dependency-0.0.1.tar.gz":
                            [
                                {
                                    "has_no_slim_dependencies.tgz": []
                                }
                            ]
                        }
                    ]
                }
            ]
        }),
    (os.path.join(APP_PACKAGE_TESTING_PACKAGES_PATH, "has_two_static_slim_dependencies_one_level_deep-0.0.1.tar.gz"),
        {
            "has_two_static_slim_dependencies_one_level_deep-0.0.1.tar.gz":
            [
                {
                    "good_app_conf-0.0.1.tar.gz": []
                },
                {
                    "has_no_slim_dependencies.tgz": []
                },
            ]
        }),
    (os.path.join(APP_PACKAGE_TESTING_PACKAGES_PATH, "has_two_static_slim_dependencies_two_levels_deep-0.0.1.tar.gz"), \
        {
            "has_two_static_slim_dependencies_two_levels_deep-0.0.1.tar.gz":
            [
                {
                    "has_no_slim_dependencies.tgz": []
                },
                {
                    "has_one_static_slim_dependency-0.0.1.tar.gz":
                    [
                        {
                            "has_no_slim_dependencies.tgz": []
                        }
                    ]
                }
            ]
        }),
]


# ==============================================================================
# App.is_static_slim_dependency
# ==============================================================================
@pytest.mark.parametrize("test_package_path,static_dependencies_definitions", static_slim_dependencies_test_parameters)
def test_is_static_slim_dependency(test_package_path, static_dependencies_definitions):
    """Test that the App.is_static_slim_dependency method's returns True for
    dependency Apps and False otherwise
    """
    package_handler = splunk_appinspect.app_package_handler.AppPackageHandler(test_package_path)
    for package in package_handler.app_packages:
        app = splunk_appinspect.App(package=package)
        package_filename = os.path.basename(package.origin_path)
        app_is_dependency = not package_filename in static_dependencies_definitions.keys()
        assertion_output = ("`test_is_static_slim_dependency`"
                            " expected: `{}`"
                            " received: `{}`").format(app_is_dependency,
                                                      app.is_static_slim_dependency)
        assert app_is_dependency == app.is_static_slim_dependency, assertion_output


# ==============================================================================
# App.static_slim_app_dependencies
# ==============================================================================
@pytest.mark.parametrize("test_package_path,static_dependencies_definitions", static_slim_dependencies_test_parameters)
def test_static_slim_app_dependencies(test_package_path, static_dependencies_definitions):
    """Test that the App.static_slim_app_dependencies method's returns expected
    dependencies hierarchy.
    """
    def _assert_dependencies_match_dict_and_recurse(app, list_to_match):
        """Help function that takes an app (App) and list_to_match (List) and
        asserts that the dict in the list_to_match match the dependencies of the
        app, then recurses over the values of the list_to_match dicts and app
        dependencies to match those.
        """
        # Assert that each of the dependencies for this App are what we expect,
        # use the basename of the package as the source of truth, this is about
        # the best we can do since many of these apps have the same id/name
        expected_origin_filenames = set()
        for dependency_dict in list_to_match:
            for key in dependency_dict.keys():
                expected_origin_filenames.add(key)
        app_dependencies = app.static_slim_app_dependencies
        dependency_origin_filenames = set([os.path.basename(dependency.package.origin_path)
                                           for dependency in app_dependencies])

        assertion_output = ("`test_static_slim_app_dependencies`"
                            " expected: `{}`"
                            " received: `{}`").format(expected_origin_filenames,
                                                      dependency_origin_filenames)
        assert expected_origin_filenames == dependency_origin_filenames, assertion_output

        # Recurse, for any dependencies check these for their dependencies
        for dependency_dict in list_to_match:
            for dependency_dict_key, dependency_dict_value in iteritems(dependency_dict):
                # Find the app within this app's dependencies that corresponds
                # to the key in the dict_to_match that we are iterating
                found_app = None
                for app_dependency in app_dependencies:
                    origin_name = os.path.basename(app_dependency.package.origin_path)
                    if origin_name == dependency_dict_key:
                        found_app = app_dependency
                        break
                # Check if no app found, this shouldn't be possible
                assertion_output = ("`test_static_slim_app_dependencies` app"
                                    " not found for dependency `{}` within"
                                    " test_package_path: `{}`"
                                    .format(dependency_dict_key, test_package_path))
                assert found_app is not None, assertion_output
                _assert_dependencies_match_dict_and_recurse(found_app, dependency_dict_value)

    # Initialize the package handler to gather all AppPackages and dependencies
    package_handler = splunk_appinspect.app_package_handler.AppPackageHandler(test_package_path)

    # For the first keys in static_dependencies_definitions find the appropriate
    # packages, these should have the same base artifact name and correct number
    # of dependencies, then traverse from there
    for dependency_origin_basename, dependency_dict in iteritems(static_dependencies_definitions):
        found_package = None
        for package_candidate in package_handler.app_packages:
            origin_name = os.path.basename(package_candidate.origin_path)
            if origin_name == dependency_origin_basename:
                found_package = package_candidate
                break
        # Check if no app found, this shouldn't be possible
        assertion_output = ("`test_static_slim_app_dependencies` package not"
                            " found for input dependency_origin_basename key"
                            " `{}` within test_package_path: `{}`"
                            .format(dependency_origin_basename, test_package_path))
        assert found_package is not None, assertion_output
        app = splunk_appinspect.App(package=found_package)

        # Make sure this app matches dependencies keys we expect and recurse
        _assert_dependencies_match_dict_and_recurse(app, dependency_dict)


# ==============================================================================
# App._get_hash
# ==============================================================================
app_get_hash_return_values_test_parameters = [
    (os.path.join(APPINSPECT_TEST_PACKAGES_PATH, "good_app_conf")),
    (os.path.join(APP_PACKAGE_TESTING_PACKAGES_PATH, "good_app_conf.spl")),
    (os.path.join(APP_PACKAGE_TESTING_PACKAGES_PATH, "good_app_conf.tgz")),
    (os.path.join(APP_PACKAGE_TESTING_PACKAGES_PATH, "good_app_conf.tar.gz")),
    (os.path.join(APP_PACKAGE_TESTING_PACKAGES_PATH, "good_app_conf.zip")),
    (os.path.join(APP_PACKAGE_TESTING_PACKAGES_PATH, "has_nested_good_tgz_spl_zip_splunk_apps-ACD-1310")),
    (os.path.join(APP_PACKAGE_TESTING_PACKAGES_PATH, "has_nested_good_tgz_spl_zip_splunk_apps-ACD-1310.tgz")),
    (os.path.join(APP_PACKAGE_TESTING_PACKAGES_PATH, "has_hidden_dependencies_directory-ACD-1556")),
    (os.path.join(APP_PACKAGE_TESTING_PACKAGES_PATH, "has_hidden_dependencies_directory-ACD-1556.spl")),
    (os.path.join(APP_PACKAGE_TESTING_PACKAGES_PATH, "has_hidden_dependencies_directory-ACD-1556.tar.gz")),
    (os.path.join(APP_PACKAGE_TESTING_PACKAGES_PATH, "has_hidden_dependencies_directory-ACD-1556.tgz")),
    (os.path.join(APP_PACKAGE_TESTING_PACKAGES_PATH, "has_hidden_dependencies_directory-ACD-1556.zip")),
    (os.path.join(APP_PACKAGE_TESTING_PACKAGES_PATH, "ta_aob_sample_2_2_0-1.0.0.spl")),
    (os.path.join(APP_PACKAGE_TESTING_PACKAGES_PATH, "has_missing_app_conf_file-ACD-1362")),
    (os.path.join(APP_PACKAGE_TESTING_PACKAGES_PATH, "has_missing_app_conf_file-ACD-1362.spl")),
    (os.path.join(APP_PACKAGE_TESTING_PACKAGES_PATH, "has_missing_app_conf_file-ACD-1362.tgz")),
    (os.path.join(APP_PACKAGE_TESTING_PACKAGES_PATH, "has_missing_app_conf_file-ACD-1362.tar.gz")),
    (os.path.join(APP_PACKAGE_TESTING_PACKAGES_PATH, "has_missing_app_conf_file-ACD-1362.zip")),
]


@pytest.mark.parametrize("test_package_path", app_get_hash_return_values_test_parameters)
def test_app_get_hash_return_values(test_package_path):
    """Test that the App._get_hash's method returns expected values."""
    app = splunk_appinspect.App(test_package_path)
    hash_value = app._get_hash()
    assert type(hash_value) is str
    assert hash_value != ""


# ==============================================================================
# App Helper Functions
# ==============================================================================
@pytest.mark.parametrize("test_package_path", general_app_package_test_parameters)
def test_app_returns_correct_alert_actions_domain_object(test_package_path):
    """Tests App object helper function returns correct object type for
    App.get_alert_actions().
    """
    app = splunk_appinspect.App(test_package_path)
    alert_actions = app.get_alert_actions()
    assert isinstance(alert_actions,
                      splunk_appinspect.alert_actions.AlertActions)


@pytest.mark.parametrize("test_package_path", general_app_package_test_parameters)
def test_app_returns_correct_custom_commands_domain_object(test_package_path):
    """Tests App object helper function returns correct object type for
    App.get_custom_commands().
    """
    app = splunk_appinspect.App(test_package_path)
    custom_commands = app.get_custom_commands()
    assert isinstance(custom_commands,
                      splunk_appinspect.custom_commands.CustomCommands)


@pytest.mark.parametrize("test_package_path", general_app_package_test_parameters)
def test_app_returns_correct_custom_visualizations_domain_object(test_package_path):
    """Tests App object helper function returns correct object type for
    App.get_custom_visualizations().
    """
    app = splunk_appinspect.App(test_package_path)
    custom_visualizations = app.get_custom_visualizations()
    assert isinstance(custom_visualizations,
                      splunk_appinspect.custom_visualizations.CustomVisualizations)


@pytest.mark.parametrize("test_package_path", general_app_package_test_parameters)
def test_app_returns_correct_modular_inputs_domain_object(test_package_path):
    """Tests App object helper function returns correct object type for
    App.get_modular_inputs().
    """
    app = splunk_appinspect.App(test_package_path)
    modular_inputs = app.get_modular_inputs()
    assert isinstance(modular_inputs,
                      splunk_appinspect.modular_inputs.ModularInputs)


@pytest.mark.parametrize("test_package_path", general_app_package_test_parameters)
def test_app_returns_correct_rest_map_domain_object(test_package_path):
    """Tests App object helper function returns correct object type for
    App.get_rest_map().
    """
    app = splunk_appinspect.App(test_package_path)
    rest_map = app.get_rest_map()
    assert isinstance(rest_map,
                      splunk_appinspect.rest_map.RestMap)


@pytest.mark.parametrize("test_package_path", general_app_package_test_parameters)
def test_app_returns_correct_saved_searches_domain_object(test_package_path):
    """Tests App object helper function returns correct object type for
    App.get_saved_searches().
    """
    app = splunk_appinspect.App(test_package_path)
    rest_map = app.get_saved_searches()
    assert isinstance(rest_map,
                      splunk_appinspect.saved_searches.SavedSearches)


@pytest.mark.parametrize("test_package_path", general_app_package_test_parameters)
def test_app_returns_correct_workflow_actions_domain_object(test_package_path):
    """Tests App object helper function returns correct object type for
    App.get_workflow_actions().
    """
    app = splunk_appinspect.App(test_package_path)
    workflow_actions = app.get_workflow_actions()
    assert isinstance(workflow_actions,
                      splunk_appinspect.workflow_actions.WorkFlowActions)


def test_python_code_not_in_trusted_libs():
    """Tests App object could not filter python code"""
    test_package_path = os.path.join(APP_PACKAGE_TESTING_PACKAGES_PATH,
                                     "has_python_file_could_not_been_filtered_by_trusted_libs_ACD-3253")

    def check_for_test():
        """mock real scenario"""
        app = splunk_appinspect.App(test_package_path, python_analyzer_enable=False)
        for dir, file, ext in app.iterate_files():
            assert file == "code.py"

    check_for_test()


def test_python_code_filtered_by_trusted_libs():
    """Tests App object filter trusted libs files"""
    test_package_path = os.path.join(APP_PACKAGE_TESTING_PACKAGES_PATH,
                                     "has_python_file_could_not_been_filtered_by_trusted_libs_ACD-3253")

    def check_for_test():
        """mock real scenario"""
        import hashlib
        sha256 = hashlib.sha256()
        app = splunk_appinspect.App(test_package_path, python_analyzer_enable=False)
        # hack trusted lib manager
        test_file_path = os.path.join(app.app_dir, "bin", "code.py")
        with open(test_file_path, "rb") as f:
            sha256.update(f.read())
        app._trusted_libs_manager.libs_data._trusted_check_and_libs.add(("check_for_test", sha256.hexdigest()))
        # test file should be filtered
        assert list(app.iterate_files()) == []

    check_for_test()


def test_trusted_libs_filter_check_for_environment_variable_use_in_python():
    """check if `check for environment variable use in python` could be filtered"""
    test_package_path = os.path.join(APP_PACKAGE_TESTING_PACKAGES_PATH,
                                     "ACD-3253")

    def check_for_environment_variable_use_in_python():
        # disable python analyzer, since we don't we want use 2to3
        app = splunk_appinspect.App(test_package_path, python_analyzer_enable=False)
        for dir, file, ext in app.iterate_files(basedir=os.path.join("bin", "ta_dellemc_vmax"), types=[".py"]):
            assert file == "ipaddress.py"

    check_for_environment_variable_use_in_python()

def test_trusted_libs_filter_check_hostnames_and_ips():
    """check if `check hostnames and ips` could be filtered"""
    test_package_path = os.path.join(APP_PACKAGE_TESTING_PACKAGES_PATH,
                                     "ACD-3253")

    def check_hostnames_and_ips():
        # disable python analyzer, since we don't we want use 2to3
        app = splunk_appinspect.App(test_package_path, python_analyzer_enable=False)
        for dir, file, ext in app.iterate_files(basedir=os.path.join("bin", "ta_dellemc_vmax"), types=[".py"]):
            assert file == "ipaddress.py"

    check_hostnames_and_ips()

def test_trusted_libs_filter_check_for_secret_disclosure():
    """check if `check for secret disclosure` could be filtered"""
    test_package_path = os.path.join(APP_PACKAGE_TESTING_PACKAGES_PATH,
                                     "ACD-3253")

    def check_for_secret_disclosure():
        # disable python analyzer, since we don't we want use 2to3
        app = splunk_appinspect.App(test_package_path, python_analyzer_enable=False)
        for dir, file, ext in app.iterate_files(basedir=os.path.join("bin", "ta_dellemc_vmax"), types=[".py"]):
            assert file == "ipaddress.py"

    check_for_secret_disclosure()

def test_trusted_libs_filter_check_for_sensitive_info_in_url():
    """check if `check for sensitive info in url` could be filtered"""
    test_package_path = os.path.join(APP_PACKAGE_TESTING_PACKAGES_PATH,
                                     "ACD-3253")

    def check_for_sensitive_info_in_url():
        # disable python analyzer, since we don't we want use 2to3
        app = splunk_appinspect.App(test_package_path, python_analyzer_enable=False)
        for dir, file, ext in app.iterate_files(basedir=os.path.join("bin", "ta_dellemc_vmax"), types=[".py"]):
            assert file == "ipaddress.py"

    check_for_sensitive_info_in_url()