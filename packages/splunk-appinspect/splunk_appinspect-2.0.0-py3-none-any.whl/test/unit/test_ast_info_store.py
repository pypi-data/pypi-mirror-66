from __future__ import print_function
import pytest
from splunk_appinspect.python_analyzer.ast_info_store import AstInfoStore
from os.path import dirname, join, abspath

APPINSPECT_TEST_PATH = dirname(abspath(__file__))
APPINSPECT_TEST_PACKAGES_PATH = join(APPINSPECT_TEST_PATH, "python_analyzer_packages", "utilities", "find_imports")


@pytest.mark.parametrize("import_chain,filepath,pkg_path_and_obj_name", [
    (
        "pkg_a",
        join(APPINSPECT_TEST_PACKAGES_PATH, 'alphabet', 'a.py'),
        (
            join(APPINSPECT_TEST_PACKAGES_PATH, 'alphabet', 'pkg_a', '__init__.py'),
            None,
        )
    ),
    (
        "pkg_a.mod_c.*",
        join(APPINSPECT_TEST_PACKAGES_PATH, 'alphabet', 'h.py'),
        (
            join(APPINSPECT_TEST_PACKAGES_PATH, 'alphabet', 'pkg_a', 'mod_c.py'),
            "*",
        )
    ),
    (
        ".pkg_a.mod_c",
        join(APPINSPECT_TEST_PACKAGES_PATH, 'alphabet', 'j.py'),
        (
            join(APPINSPECT_TEST_PACKAGES_PATH, 'alphabet', 'pkg_a', 'mod_c.py'),
            None,
        )
    ),
    (
        "..mod_e.mod_e_var",
        join(APPINSPECT_TEST_PACKAGES_PATH, 'alphabet', 'k.py'),
        (
            join(APPINSPECT_TEST_PACKAGES_PATH, 'mod_e.py'),
            "mod_e_var",
        )
    ),
    (
        "....mod_e.mod_e_var",
        join(APPINSPECT_TEST_PACKAGES_PATH, 'alphabet', 'pkg_a', 'pkg_b', 'o.py'),
        (
            join(APPINSPECT_TEST_PACKAGES_PATH, 'mod_e.py'),
            "mod_e_var",
        )
    ),
    (
        ".*",
        join(APPINSPECT_TEST_PACKAGES_PATH, 'mod_e.py'),
        (
            join(APPINSPECT_TEST_PACKAGES_PATH, '__init__.py'),
            "*",
        )
    ),
])
def test_get_pkg_path_and_obj_name(import_chain, filepath, pkg_path_and_obj_name):
    astInfoStore = AstInfoStore()
    astInfoStore.set_pointer(filepath)
    print(astInfoStore.get_pkg_path_and_obj_name(import_chain))
    assert astInfoStore.get_pkg_path_and_obj_name(import_chain) == pkg_path_and_obj_name


def test_get_pkg_path_and_obj_name_with_persistent_pointers():
    astInfoStore = AstInfoStore(libs=[join(APPINSPECT_TEST_PACKAGES_PATH, 'alphabet', 'pkg_a')])
    astInfoStore.set_pointer(join(APPINSPECT_TEST_PACKAGES_PATH, 'alphabet', 'pkg_a', 'pkg_b'))
    expected_res = (
                        join(APPINSPECT_TEST_PACKAGES_PATH, 'alphabet', 'pkg_a', 'mod_d.py'),
                        None
                    )
    assert astInfoStore.get_pkg_path_and_obj_name('mod_d') == expected_res