import os
from splunk_appinspect.python_analyzer.trustedlibs import trusted_libs_manager
from splunk_appinspect.python_analyzer.trustedlibs import utilities
APPINSPECT_TEST_PATH = os.path.dirname(os.path.abspath(__file__))
APPINSPECT_TEST_PACKAGES_PATH = os.path.join(APPINSPECT_TEST_PATH, "python_analyzer_packages", "trustedlibs")

TRUSTED_CHECK_AND_LIBS_FILE = os.path.join(APPINSPECT_TEST_PACKAGES_PATH, 'trusted_check_and_libs.csv')
UNTRUSTED_CHECK_AND_LIBS_FILE = os.path.join(APPINSPECT_TEST_PACKAGES_PATH, 'untrusted_check_and_libs.csv')


def test_init_trustedlibs_manager_with_illegal_files():
    # Illegal file path won't block trustedlibs' initialization
    manager = trusted_libs_manager.TrustedLibsManager('a', 'b')
    assert manager.libs_data.get_trusted_check_and_libs() == set()
    assert manager.libs_data.get_untrusted_check_and_libs() == set()


def test_get_hash_file():
    """
    :return: sha256 hash of an zipped app package file
    """
    file_path = os.path.join(APPINSPECT_TEST_PACKAGES_PATH, 'splunklib', "environment.py")
    assert utilities.get_hash_file(_get_file_content(file_path)) == "997e76b662628010e782e22bcefccc1c5bbd5f2b039068ba58d9791ae50a293b"


def test_trusted_check_and_lib_tuple():
    api = trusted_libs_manager.TrustedLibsManager(TRUSTED_CHECK_AND_LIBS_FILE, UNTRUSTED_CHECK_AND_LIBS_FILE)

    # 997e76b662628010e782e22bcefccc1c5bbd5f2b039068ba58d9791ae50a293b
    result = api.check_if_lib_is_trusted("check_for_hidden_python_files",
                                         _get_file_content(os.path.join(APPINSPECT_TEST_PACKAGES_PATH, 'splunklib', "environment.py")))
    assert result


def test_check_and_lib_tuple_appeared_in_trusted_and_untrusted_files():
    api = trusted_libs_manager.TrustedLibsManager(TRUSTED_CHECK_AND_LIBS_FILE, UNTRUSTED_CHECK_AND_LIBS_FILE)
    # 231ecc5ef810fe628e2972360d9860b6b92c92cd6e39badac2b0e8f53c790364
    result = api.check_if_lib_is_trusted("check_for_hidden_python_files",
                                         _get_file_content(os.path.join(APPINSPECT_TEST_PACKAGES_PATH, 'splunklib', "internals.py")))
    assert result is False


def test_legal_check_name_with_untrusted_lib():
    api = trusted_libs_manager.TrustedLibsManager(TRUSTED_CHECK_AND_LIBS_FILE, UNTRUSTED_CHECK_AND_LIBS_FILE)
    result = api.check_if_lib_is_trusted("check_for_hidden_python_files",
                                         "import os".encode("utf-8"))
    assert result is False


def test_illegal_check_name_with_trusted_lib():
    api = trusted_libs_manager.TrustedLibsManager(TRUSTED_CHECK_AND_LIBS_FILE, UNTRUSTED_CHECK_AND_LIBS_FILE)
    # aafe6a0336b5e3eb7e6fd8bfb4c86c0b6fd8e3c2c77a08181b931d8a5d803e6e
    result = api.check_if_lib_is_trusted("untrusted_check",
                                         _get_file_content(os.path.join(APPINSPECT_TEST_PACKAGES_PATH, 'splunklib', "eventing_command.py")))
    assert result is False


def test_illegal_check_name_with_untrusted_lib():
    api = trusted_libs_manager.TrustedLibsManager(TRUSTED_CHECK_AND_LIBS_FILE, UNTRUSTED_CHECK_AND_LIBS_FILE)
    result = api.check_if_lib_is_trusted("untrusted_check",
                                         "import os".encode("utf-8"))
    assert result is False


def _get_file_content(file_path):
    with open(file_path, "rb") as f:
        return f.read()
