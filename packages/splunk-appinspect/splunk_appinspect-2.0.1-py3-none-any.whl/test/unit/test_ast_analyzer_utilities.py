import pytest

from splunk_appinspect.python_analyzer.utilities import find_imports, find_python_function_in_loop
from splunk_appinspect.python_analyzer.utilities import get_from_import_module_name
from splunk_appinspect.python_analyzer.utilities import relative_import_dump
from splunk_appinspect.python_analyzer.utilities import find_pkg_path
from splunk_appinspect.python_analyzer.utilities import fetch_all_nodes_belonging_to_given_subtree

from splunk_appinspect.python_analyzer.ast_analyzer import AstAnalyzer

import os.path
import ast

APPINSPECT_TEST_PATH = os.path.dirname(os.path.abspath(__file__))
APPINSPECT_TEST_PACKAGES_PATH = os.path.join(APPINSPECT_TEST_PATH, "python_analyzer_packages", "utilities")


def _verify_payloads(candidate, criteria):
    for payload in criteria:
        if payload not in candidate:
            return False
    for payload in candidate:
        if payload not in criteria:
            return False
    return True


@pytest.mark.parametrize("target_package_path,expected_pkg_str", [
    (os.path.join(APPINSPECT_TEST_PACKAGES_PATH, "find_imports", "alphabet", "d.py"), "pkg_a"),
    (os.path.join(APPINSPECT_TEST_PACKAGES_PATH, "find_imports", "alphabet", "f.py"), "pkg_a.mod_c"),
    (os.path.join(APPINSPECT_TEST_PACKAGES_PATH, "find_imports", "alphabet", "j.py"), ".pkg_a"),
    (os.path.join(APPINSPECT_TEST_PACKAGES_PATH, "find_imports", "alphabet", "k.py"), "..mod_e"),
    (os.path.join(APPINSPECT_TEST_PACKAGES_PATH, "find_imports", "alphabet", "l.py"), "..mod_e"),
    (os.path.join(APPINSPECT_TEST_PACKAGES_PATH, "find_imports", "alphabet", "m.py"), "."),
    (os.path.join(APPINSPECT_TEST_PACKAGES_PATH, "find_imports", "alphabet", "n.py"), "pkg_a"),
    (os.path.join(APPINSPECT_TEST_PACKAGES_PATH, "find_imports", "alphabet", "BOM.py"), ".features"),
    (os.path.join(APPINSPECT_TEST_PACKAGES_PATH, "find_imports", "alphabet", "pkg_a", "pkg_b", "o.py"), "....mod_e"),
    (os.path.join(APPINSPECT_TEST_PACKAGES_PATH, "find_imports", "alphabet", "p.py"), "pkg_a"),
    (os.path.join(APPINSPECT_TEST_PACKAGES_PATH, "find_imports", "alphabet", "q.py"), "pyPgSQL"),
])
def test_get_from_import_module(target_package_path, expected_pkg_str):
    analyzer = AstAnalyzer(target_package_path)
    for ast_node in ast.walk(analyzer.root_ast_node):
        if isinstance(ast_node, ast.ImportFrom):
            assert get_from_import_module_name(ast_node, analyzer.python_code_lines) == expected_pkg_str


@pytest.mark.parametrize("import_chain,filepath,expected_import_chain,expected_importing_path", [
    ("mod_b", "/pkg_a/pkg_b/mod_a.py", "mod_b", "/pkg_a/pkg_b/mod_a.py"),
    (".mod_b", "/pkg_a/pkg_b/mod_a.py", "mod_b", "/pkg_a/pkg_b/mod_a.py"),
    ("..mod_c", "/pkg_a/pkg_b/mod_a.py", "mod_c", "/pkg_a/pkg_b"),
])
def test_relative_import_dump(import_chain, filepath, expected_import_chain, expected_importing_path):
    procd_import_chain, importing_path = relative_import_dump(import_chain, filepath)
    assert (procd_import_chain, importing_path) == (
        expected_import_chain,
        expected_importing_path
    )


@pytest.mark.parametrize("filepath_perfroming_import,pkg_name,pkg_path", [
    (
        os.path.join(APPINSPECT_TEST_PACKAGES_PATH, "find_imports", "alphabet", "a.py"),
        "pkg_a",
        os.path.join(APPINSPECT_TEST_PACKAGES_PATH, "find_imports", "alphabet", "pkg_a", "__init__.py")
    ),
    (
        os.path.join(APPINSPECT_TEST_PACKAGES_PATH, "find_imports", "alphabet", "b.py"),
        "pkg_a.pkg_b",
        os.path.join(APPINSPECT_TEST_PACKAGES_PATH, "find_imports", "alphabet", "pkg_a", "pkg_b", "__init__.py")
    ),
    (
        os.path.join(APPINSPECT_TEST_PACKAGES_PATH, "find_imports", "alphabet"),
        "mod_e",
        os.path.join(APPINSPECT_TEST_PACKAGES_PATH, "find_imports", "mod_e.py")
    ),
    (
        os.path.join(APPINSPECT_TEST_PACKAGES_PATH, "find_imports", "alphabet", "pkg_a", "__init__.py"),
        "socket",
        None
    ),
])
def test_find_pkg_path(filepath_perfroming_import, pkg_name, pkg_path):
    assert find_pkg_path(filepath_perfroming_import, pkg_name) == pkg_path


@pytest.mark.parametrize("filepath_perfroming_import,pkg_name,libs,pkg_path", [
    (
        os.path.join(APPINSPECT_TEST_PACKAGES_PATH, "find_imports", "alphabet", "pkg_a", "pkg_b", "s.py"),
        "mod_d",
        [os.path.join(APPINSPECT_TEST_PACKAGES_PATH, "find_imports", "alphabet", "pkg_a")],
        os.path.join(APPINSPECT_TEST_PACKAGES_PATH, "find_imports", "alphabet", "pkg_a", "mod_d.py")
    )
])
def test_find_pkg_path_with_libs(filepath_perfroming_import, pkg_name, libs, pkg_path):
    assert find_pkg_path(filepath_perfroming_import, pkg_name, libs=libs) == pkg_path


@pytest.mark.parametrize("target_package_path,payloads", [
    (
        os.path.join(APPINSPECT_TEST_PACKAGES_PATH, "find_imports", "alphabet", "a.py"),
        [
            ("pkg_a", "pkg_a", None, os.path.join(APPINSPECT_TEST_PACKAGES_PATH,
            os.path.join("find_imports", "alphabet", "pkg_a", "__init__.py")), 1)
        ]
    ),
    (
        os.path.join(APPINSPECT_TEST_PACKAGES_PATH, "find_imports", "alphabet", "b.py"),
        [
            ("pkg_a.pkg_b", "pkg_a.pkg_b", None, os.path.join(APPINSPECT_TEST_PACKAGES_PATH,
            os.path.join("find_imports", "alphabet", "pkg_a", "pkg_b", "__init__.py")), 1)
        ]
    ),
    (
        os.path.join(APPINSPECT_TEST_PACKAGES_PATH, "find_imports", "alphabet", "c.py"),
        [
            ("pkg_a.mod_c", "pkg_a.mod_c", None, os.path.join(APPINSPECT_TEST_PACKAGES_PATH,
                        os.path.join("find_imports", "alphabet", "pkg_a", "mod_c.py")), 1),
            ("pkg_a.mod_d", "pkg_a.mod_d", None, os.path.join(APPINSPECT_TEST_PACKAGES_PATH,
                        os.path.join("find_imports", "alphabet", "pkg_a", "mod_d.py")), 1)
        ]
    ),
    (
        os.path.join(APPINSPECT_TEST_PACKAGES_PATH, "find_imports", "alphabet", "d.py"),
        [
            ("pkg_a", "pkg_b", None, os.path.join(APPINSPECT_TEST_PACKAGES_PATH,
            os.path.join("find_imports", "alphabet", "pkg_a", "pkg_b", "__init__.py")), 1)
        ]
    ),
    (
        os.path.join(APPINSPECT_TEST_PACKAGES_PATH, "find_imports", "alphabet", "e.py"),
        [
            ("pkg_a", "mod_c", None, os.path.join(APPINSPECT_TEST_PACKAGES_PATH,
            os.path.join("find_imports", "alphabet", "pkg_a", "mod_c.py")), 1)
        ]
    ),
    (
        os.path.join(APPINSPECT_TEST_PACKAGES_PATH, "find_imports", "alphabet", "f.py"),
        [
            ("pkg_a.mod_c", None, "one_class", os.path.join(APPINSPECT_TEST_PACKAGES_PATH,
            os.path.join("find_imports", "alphabet", "pkg_a", "mod_c.py")), 1)
        ]
    ),
    (
        os.path.join(APPINSPECT_TEST_PACKAGES_PATH, "find_imports", "alphabet", "g.py"),
        [   
            ("pkg_a.pkg_b", None, "*", os.path.join(APPINSPECT_TEST_PACKAGES_PATH,
            os.path.join("find_imports", "alphabet", "pkg_a", "pkg_b", "__init__.py")), 1)
        ]
    ),
    (
        os.path.join(APPINSPECT_TEST_PACKAGES_PATH, "find_imports", "alphabet", "h.py"),
        [
            ("pkg_a.mod_c", None, "*", os.path.join(APPINSPECT_TEST_PACKAGES_PATH,
            os.path.join("find_imports", "alphabet", "pkg_a", "mod_c.py")), 1)
        ]
    ),
    (
        os.path.join(APPINSPECT_TEST_PACKAGES_PATH, "find_imports", "alphabet", "i.py"),
        [
            ("pkg_a", "mod_c", None, os.path.join(APPINSPECT_TEST_PACKAGES_PATH,
            os.path.join("find_imports", "alphabet", "pkg_a", "mod_c.py")), 1),
            ("pkg_a", "mod_d", None, os.path.join(APPINSPECT_TEST_PACKAGES_PATH,
            os.path.join("find_imports", "alphabet", "pkg_a", "mod_d.py")), 1)
        ]
    ),
    (
        os.path.join(APPINSPECT_TEST_PACKAGES_PATH, "find_imports", "alphabet", "j.py"),
        [
            ("pkg_a", "mod_c", None, os.path.join(APPINSPECT_TEST_PACKAGES_PATH,
            os.path.join("find_imports", "alphabet", "pkg_a", "mod_c.py")), 1)
        ]
    ),
    (
        os.path.join(APPINSPECT_TEST_PACKAGES_PATH, "find_imports", "alphabet", "k.py"),
        [
            ("mod_e", None, "mod_e_var", os.path.join(APPINSPECT_TEST_PACKAGES_PATH,
            os.path.join("find_imports", "mod_e.py")), 1)
        ]
    )
])
def test_find_imports(target_package_path, payloads):
    deps = find_imports(target_package_path)
    assert _verify_payloads(deps, payloads)


def test_fetch_all_nodes_belonging_to_given_subtree():
    path = os.path.join(APPINSPECT_TEST_PACKAGES_PATH, 'fetch_all_nodes_belonging_to_given_subtree', 'class_func_example.py')
    ast_root = ast.parse(open(path).read())

    # find class node
    class_node = None
    for node in ast.walk(ast_root):
        if isinstance(node, ast.ClassDef):
            class_node = node
            break

    # collect all possible functions
    func_node_set = set()
    for node in ast.walk(ast_root):
        if isinstance(node, ast.FunctionDef):
            func_node_set.add(node)

    # collect all possible functions in class
    class_func_node_set = set()
    for node in ast.walk(class_node):
        if isinstance(node, ast.FunctionDef):
            class_func_node_set.add(node)

    intersection_result = fetch_all_nodes_belonging_to_given_subtree(class_node, func_node_set)
    assert len(intersection_result) == len(class_func_node_set)

    list1 = list(map(lambda node: node.name, intersection_result))
    list2 = list(map(lambda node: node.name, class_func_node_set))

    list1.sort()
    list2.sort()

    assert list1 == list2


def test_function_call_in_for_loop():
    path = os.path.join(APPINSPECT_TEST_PACKAGES_PATH, 'fetch_all_nodes_belonging_to_given_subtree',
                        'function_call_in_for_loop.py')
    analyzer = AstAnalyzer(python_file_path=path)

    # collect all risky usage
    os_fork_node_set = set(analyzer.get_module_function_call_usage('os', 'fork'))
    thread_start_node_set = set(analyzer.get_module_function_call_usage('thread', 'start_new_thread'))
    node_set = os_fork_node_set | thread_start_node_set

    assert len(node_set) == 4
    assert len(os_fork_node_set) == 3
    assert len(thread_start_node_set) == 1

    # find all for loop node
    intersection_node_set = set()
    for node in ast.walk(analyzer.root_ast_node):
        if isinstance(node, ast.For):
            result_set = fetch_all_nodes_belonging_to_given_subtree(node, node_set)

            if node.lineno == 5 or node.lineno == 9:
                assert len(result_set) == 1
                call_node = list(result_set)[0]
                if node.lineno == 5:
                    assert call_node.lineno == 6
                elif node.lineno == 9:
                    assert call_node.lineno == 10

            intersection_node_set |= result_set

    node_list = list(map(lambda node: node.lineno, intersection_node_set))
    node_list.sort()
    assert node_list == [6, 10]


def test_find_python_function_in_loop():
    path = os.path.join(APPINSPECT_TEST_PACKAGES_PATH, 'find_python_function_in_loop', 'python_func_in_loop.py')
    analyzer = AstAnalyzer(python_file_path=path)
    result_set = find_python_function_in_loop(analyzer, "os", "fork")
    result_list = list(result_set)
    result_list.sort(key=lambda k: k.lineno)
    result_list = map(lambda node: node.lineno, result_list)
    assert list(result_list) == [5, 6]