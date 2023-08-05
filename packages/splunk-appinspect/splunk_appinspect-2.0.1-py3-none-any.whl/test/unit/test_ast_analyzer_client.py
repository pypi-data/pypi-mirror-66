import pytest
import six
import tempfile
import os
import shutil

from splunk_appinspect.python_analyzer.client import Client
from splunk_appinspect.python_analyzer.trustedlibs.utilities import get_hash_file

from os.path import dirname, join, abspath


APPINSPECT_TEST_PATH = dirname(abspath(__file__))
APPINSPECT_TEST_PACKAGES_PATH = join(APPINSPECT_TEST_PATH, "python_analyzer_packages", "client")

DUMMY_CHECK = 'check_dummy'

def _fetch_load(analyzer, obj_name):
    if obj_name is None:
        return analyzer.module
    return analyzer.module.global_map[obj_name]


class dummy_trustedlib(object):
    def check_if_lib_is_trusted(self, check_name, file_content=None, content_hash=None):
        if check_name == "check_in_trustedlib":
            return True
        return False


def check_in_trustedlib(client):
    interated_files = []
    for filepath, ast_info in client.get_all_ast_infos():
        interated_files.append(filepath)
    return interated_files


def check_not_in_trustedlib(client):
    interated_files = []
    for filepath, ast_info in client.get_all_ast_infos():
        interated_files.append(filepath)
    return interated_files


class metadata_obj(object):
    def instantiate(self):
        return "This is a metadata object"


class python_metadata_module(object):
    def query_namespace(self, namespace):
        if namespace == "os":
            return [metadata_obj()]
        return []


@pytest.mark.parametrize("import_chain,pointer", [
    (
        'os',
        join(APPINSPECT_TEST_PACKAGES_PATH, 'load_modules', 'a.py')
    ),
    (
        'os.path.join',
        join(APPINSPECT_TEST_PACKAGES_PATH, 'load_modules', 'e.py')
    ),
])
def test_load_builtin_modules_without_modules_metadata(import_chain, pointer):
    fixed_load_pkg_path = join(APPINSPECT_TEST_PACKAGES_PATH, 'load_modules', 'pkg_a')
    client = Client(files_folder=fixed_load_pkg_path)
    client.ast_info_store.set_pointer(pointer)
    assert len(client.load_modules(import_chain)) == 0


@pytest.mark.parametrize("import_chain,pointer,expected_modules", [
    (
        'os',
        join(APPINSPECT_TEST_PACKAGES_PATH, 'load_modules', 'a.py'),
        ["This is a metadata object"]
    ),
    (
        'os.path.join',
        join(APPINSPECT_TEST_PACKAGES_PATH, 'load_modules', 'e.py'),
        []
    ),
])
def test_load_builtin_modules_with_modules_metadata(import_chain, pointer, expected_modules):
    fixed_load_pkg_path = join(APPINSPECT_TEST_PACKAGES_PATH, 'load_modules', 'pkg_a')
    client = Client(files_folder=fixed_load_pkg_path, modules_metadata=python_metadata_module())
    client.ast_info_store.set_pointer(pointer)
    assert client.load_modules(import_chain) == expected_modules


@pytest.mark.parametrize("import_chain,pointer,obj_name", [
    (
        'pkg_a',
        join(APPINSPECT_TEST_PACKAGES_PATH, 'load_modules', 'b.py'),
        None
    ),
    (
        'pkg_a.*',
        join(APPINSPECT_TEST_PACKAGES_PATH, 'load_modules', 'c.py'),
        'pkg_a_var1'
    ),
    (
        'pkg_a.pkg_a_var2',
        join(APPINSPECT_TEST_PACKAGES_PATH, 'load_modules', 'd.py'),
        'pkg_a_var2'
    ),
])
def test_load_self_defined_modules(import_chain, pointer, obj_name):
    fixed_load_pkg_path = join(APPINSPECT_TEST_PACKAGES_PATH, 'load_modules', 'pkg_a')
    client = Client(files_folder=fixed_load_pkg_path)
    client.ast_info_store.set_pointer(pointer)
    analyzer = client.get_ast_info(join(fixed_load_pkg_path, "__init__.py"))
    loads = client.load_modules(import_chain)
    assert loads == [_fetch_load(analyzer, obj_name)]


@pytest.mark.parametrize("abs_filepath,expected_filepath", [
    (
        join(APPINSPECT_TEST_PACKAGES_PATH, 'load_modules', 'pkg_a', '__init__.py'),
        join('pkg_a', '__init__.py')
    ),
    (
        join('pkg_a', '__init__.py'),
        join('pkg_a', '__init__.py')
    )
])
def test_relativize_filepath(abs_filepath, expected_filepath):
    fixed_load_pkg_path = join(APPINSPECT_TEST_PACKAGES_PATH, 'load_modules')
    client = Client(files_folder=fixed_load_pkg_path)
    assert client._relativize_filepath(abs_filepath) == expected_filepath


@pytest.mark.parametrize("rela_filepath,expected_filepath", [
    (
        join(APPINSPECT_TEST_PACKAGES_PATH, 'load_modules', 'pkg_a', '__init__.py'),
        join(APPINSPECT_TEST_PACKAGES_PATH, 'load_modules', 'pkg_a', '__init__.py')
    ),
    (
        join('pkg_a', '__init__.py'),
        join(APPINSPECT_TEST_PACKAGES_PATH, 'load_modules', 'pkg_a', '__init__.py')
    )
])
def test_absolutize_filepath(rela_filepath, expected_filepath):
    fixed_load_pkg_path = join(APPINSPECT_TEST_PACKAGES_PATH, 'load_modules')
    client = Client(files_folder=fixed_load_pkg_path)
    assert client._absolutize_filepath(rela_filepath) == expected_filepath


def test_multi_errors():
    try:
        client = Client(files_folder=join(APPINSPECT_TEST_PACKAGES_PATH, 'multi_errors'))
        syntax_error_files = client.get_syntax_error_files(check_name=DUMMY_CHECK)
        null_byte_error_files = client.get_null_byte_error_files(check_name=DUMMY_CHECK)
        other_exception_files = client.get_other_exception_files()

        assert syntax_error_files == {'malformed.py'}
        assert null_byte_error_files == {'null_byte_error.py'}
        assert other_exception_files == set()

        # only one analyzer, corresponding filepath is normal.py
        cnt = 0
        for filepath, _ in client.get_all_ast_infos(check_name=DUMMY_CHECK):
            assert filepath == 'normal.py'
            cnt += 1
        assert cnt == 1

    except:
        # no exceptions should be thrown
        assert False


def test_client_work_with_metadata_and_self_defined_module():
    '''
    Some kind of simple integration test
    '''
    from splunk_appinspect.python_modules_metadata.python_modules_metadata_store import metadata_store

    client = Client(files_folder=join(APPINSPECT_TEST_PACKAGES_PATH, 'mix_of_metadata_and_self_defined_modules'),
                    modules_metadata=metadata_store)
    ast_info = list(filter(lambda tuple: tuple[0] == 'main.py', client.get_all_ast_infos(check_name=DUMMY_CHECK)))[0][1]

    # check metadata executable function
    result_ast_node = ast_info.get_variable_distribution('result')[0]
    result_variable = ast_info.get_variable_details(result_ast_node)
    assert result_variable.variable_value == join("a", "b")
    assert result_variable.variable_type_set == {result_variable.STRING_TYPE}

    # check normal function
    assert ast_info.get_module_function_call_usage('os', 'kill', lineno_only=True) == [8]

    # load function from user-defined module
    assert ast_info.get_module_function_call_usage('sys', '_current_frames', lineno_only=True) == [6]


def test_hidden_python_files():

    app_dir = join(APPINSPECT_TEST_PACKAGES_PATH, "hidden_python_files")
    temp_dir = os.path.join(tempfile.mkdtemp(), "tmp")
    shutil.copytree(app_dir, temp_dir)

    client = Client(files_folder=temp_dir)
    filepaths = sorted([filepath for filepath, _ in client.get_all_ast_infos(check_name=DUMMY_CHECK)])
    hidden_filepaths = sorted([filepath for filepath in client.get_hidden_python_files()])
    syntax_filepaths = sorted([filepath for filepath in client.get_syntax_error_files(check_name=DUMMY_CHECK)])

    shutil.rmtree(os.path.dirname(temp_dir))

    assert filepaths == [os.path.join("bin", "a.py"), os.path.join("bin", "hidden_python")]
    assert hidden_filepaths == [os.path.join("bin", "template.html")]
    assert syntax_filepaths == []


@pytest.mark.parametrize("dummy_check,expected_files", [
    (
        check_in_trustedlib,
        []
    ),
    (
        check_not_in_trustedlib,
        ['__init__.py']
    )
])
def test_get_all_ast_infos(dummy_check, expected_files):
    pkg_folder = join(APPINSPECT_TEST_PACKAGES_PATH, 'load_modules', 'pkg_a')
    client = Client(files_folder=pkg_folder)
    client.trusted_libs = dummy_trustedlib()
    assert dummy_check(client) == expected_files


def test_get_all_ast_infos_in_check_with_trustedlibs():
    pkg_folder = join(APPINSPECT_TEST_PACKAGES_PATH, 'get_all_ast_infos_in_check_with_trustedlibs')
    client = Client(files_folder=pkg_folder)
    file_path = join(pkg_folder, 'a.py')

    with open(file_path, 'rb') as f:
        hash_value = get_hash_file(f.read())
        client.trusted_libs.libs_data.get_trusted_check_and_libs().add((DUMMY_CHECK, hash_value))

    def check_dummy():
        paths = []
        for file_path, ast_info in client.get_all_ast_infos():
            assert file_path != 'a.py'
            paths.append(file_path)
        paths.sort()
        assert paths == ['b.py', 'c.py']

    check_dummy()


def test_get_all_ast_infos_in_nested_functions_with_trustedlibs():
    pkg_folder = join(APPINSPECT_TEST_PACKAGES_PATH, 'get_all_ast_infos_in_nested_functions_with_trustedlibs')
    client = Client(files_folder=pkg_folder)
    file_path = join(pkg_folder, 'a.py')

    with open(file_path, 'rb') as f:
        hash_value = get_hash_file(f.read())
        client.trusted_libs.libs_data.get_trusted_check_and_libs().add((DUMMY_CHECK, hash_value))

    def check_dummy():
        return search()

    def search():
        paths = []
        for file_path, ast_info in client.get_all_ast_infos():
            assert file_path != 'a.py'
            paths.append(file_path)
        assert paths == ['b.py']

    check_dummy()


def test_get_all_ast_infos_without_legal_check_name():
    pkg_folder = join(APPINSPECT_TEST_PACKAGES_PATH, 'good_app')
    client = Client(files_folder=pkg_folder)

    # without check name given
    try:
        client.get_all_ast_infos()
        assert False, 'get_all_ast_infos should throw exception here'
    except:
        pass

    # without check name in call chain
    def func():
        client.get_all_ast_infos()
    try:
        func()
        assert False, 'get_all_ast_infos should throw exception here'
    except:
        pass

    # illegal check name given
    try:
        client.get_all_ast_infos('haha')
        assert False, 'get_all_ast_infos should throw exception here'
    except:
        pass


@pytest.mark.parametrize("import_chain,ast_info_key,obj_name", [
    (
        'b',
        join('bin', 'b.py'),
        None
    ),
    (
        'c.c_var',
        join('lib', 'c.py'),
        'c_var'
    )
])
def test_bin_lib_folder_are_included_in_searching_path(import_chain, ast_info_key, obj_name):
    fixed_load_pkg_path = join(APPINSPECT_TEST_PACKAGES_PATH, 'bin_lib_folder')
    client = Client(files_folder=fixed_load_pkg_path)
    ast_info = client.get_ast_info(join(fixed_load_pkg_path, ast_info_key))
    client.ast_info_store.set_pointer(join(fixed_load_pkg_path, 'a.py'))
    loads = client.load_modules(import_chain)
    assert loads == [_fetch_load(ast_info, obj_name)]