# Python Standard Libraries
import os
import shutil
import tempfile
import pytest
# Third-Party Libraries
# Custom Libraries
import splunk_appinspect
if os.name == "nt":
    import win32security


def run_special_check(check_group, check_name, custom_setup, custom_cleanup, expected_result):
    """
    This function can be used to run the given check with custom app setup
    code. The input to the custom_setup is an empty directory to be used as the
    app for testing
    """
    check_to_test = None
    for group in splunk_appinspect.checks.groups():
        if group.name == check_group:
            for check in group.checks():
                if check.name == check_name:
                    check_to_test = check
                    break
        if check_to_test is not None:
            break
    resource_manager = splunk_appinspect.resource_manager.ResourceManager()
    app_dir = None
    try:
        app_dir = tempfile.mkdtemp()
        custom_setup(app_dir)
        app = splunk_appinspect.App(app_dir)
        with resource_manager.context({'apps': [app]}) as ctx:
            reporter = check_to_test.run(app, resource_manager_context=ctx)
        messages = map(lambda x: x.message, reporter.report_records())
        error_output = ("Expected result of {}, got {}. Messages: {}"
                        .format(expected_result, reporter.state(), messages))
        assert reporter.state() == expected_result, error_output
    finally:
        if app_dir is not None:
            custom_cleanup(app_dir)
            shutil.rmtree(app_dir)

def test_check_source_and_binaries__check_for_expansive_permissions():
    def setup(app_dir):
        # Create default/
        os.makedirs(os.path.join(app_dir, "default"))
        # Make default/app.conf
        app_conf_path = os.path.join(app_dir, "default", "app.conf")
        with open(app_conf_path, "w") as fout:
            fout.write("")
        if os.name != 'nt':
            # Give 0x777 permissions to app.conf
            os.chmod(app_conf_path, 0o777)
        else:
            sd = win32security.GetFileSecurity(app_conf_path, win32security.DACL_SECURITY_INFORMATION)
            dacl = sd.GetSecurityDescriptorDacl()
            ace_count = dacl.GetAceCount()
            for i in range(ace_count):
                rev, access, usersid = dacl.GetAce(i)
                user, group, type = win32security.LookupAccountSid('', usersid)
                if user not in ['SYSTEM', 'Administrators', 'Authenticated Users']:
                    # Give full control permissions to the user for app.conf
                    try:
                        user, domain, typ = win32security.LookupAccountName("", user)
                        dacl.AddAccessAllowedAce(win32security.ACL_REVISION, 2032127, user)
                    except:
                        pass
            sd.SetSecurityDescriptorDacl(1, dacl, 0)
            win32security.SetFileSecurity(app_conf_path, win32security.DACL_SECURITY_INFORMATION, sd)
            

    def cleanup(app_dir):
        pass

    expected_result = 'warning' if os.name == 'nt' else 'failure'
    run_special_check("check_source_and_binaries", "check_for_expansive_permissions",
                      setup, cleanup, expected_result)

@pytest.mark.skipif(os.name != "posix", reason="Only runs on Linux or OSX platform.")
def test_check_packaging_standards__check_that_extracted_splunk_app_does_not_contain_invalid_directories():
    def setup(app_dir):
        # Create default/
        default_dir = os.path.join(app_dir, "default")
        os.makedirs(default_dir)
        # Give 0x666 permissions to default/
        os.chmod(default_dir, 0o666)

    def cleanup(app_dir):
        default_dir = os.path.join(app_dir, "default")
        # Give 0x777 permissions to default/
        os.chmod(default_dir, 0o777)

    run_special_check("check_packaging_standards",
                      "check_that_extracted_splunk_app_does_not_contain_invalid_directories",
                      setup, cleanup, "failure")

@pytest.mark.skipif(os.name != "posix", reason="Only runs on Linux or OSX platform.")
def test_check_packaging_standards__check_that_extracted_splunk_app_does_not_contain_files_with_invalid_permissions():
    def setup(app_dir):
        # Create default/
        default_dir = os.path.join(app_dir, "default")
        os.makedirs(default_dir)
        # Make default/app.conf
        app_conf_path = os.path.join(app_dir, "default", "app.conf")
        with open(app_conf_path, "w") as fout:
            fout.write("")
        # Give 0x577 permissions to app.conf
        os.chmod(app_conf_path, 0o577)

    def cleanup(app_dir):
        app_conf_path = os.path.join(app_dir, "default", "app.conf")
        # Give 0x777 permissions to app.conf
        os.chmod(app_conf_path, 0o777)

    run_special_check("check_packaging_standards",
                      "check_that_extracted_splunk_app_does_not_contain_files_with_invalid_permissions",
                      setup, cleanup, "failure")