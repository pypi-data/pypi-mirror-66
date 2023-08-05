import pytest
import six
import tempfile
import shutil

from splunk_appinspect.python_analyzer.file_dep_manager import FileDepManager
from os.path import join, basename, dirname, abspath
import os
import ast


APPINSPECT_TEST_PATH = dirname(abspath(__file__))
APPINSPECT_TEST_PACKAGES_PATH = join(APPINSPECT_TEST_PATH, "python_analyzer_packages", "file_dep_manager")


def _verify_iteration_order(target, rules):
    item_pos_map = {}
    for idx, item in enumerate(target):
        if item in item_pos_map:
            return False
        item_pos_map[item] = idx
    for rule in rules:
        if item_pos_map[rule[0]] < item_pos_map[rule[1]]:
            return False
    return True


def _verify_comps(left, right):
    for l_comp in left:
        if l_comp not in right:
            return False
    for r_comp in right:
        if r_comp not in left:
            return False
    return True


@pytest.mark.parametrize("filepath,expected_files_added", [
    (
        join(APPINSPECT_TEST_PACKAGES_PATH, 'basic', 'import', 'a.py'),
        [
            join(APPINSPECT_TEST_PACKAGES_PATH, 'basic', 'import', 'a.py'),
            join(APPINSPECT_TEST_PACKAGES_PATH, 'basic', 'import', 'b.py'),
        ]
    )
])
def test_add_file(filepath, expected_files_added):
    dep_mgr = FileDepManager()
    dep_mgr.add_file(filepath)
    for expected_file_added in expected_files_added:
        assert expected_file_added in dep_mgr._file_pool


@pytest.mark.parametrize("folderpath,expected_files_added", [
    (
        join(APPINSPECT_TEST_PACKAGES_PATH, 'basic', 'import'),
        [
            join(APPINSPECT_TEST_PACKAGES_PATH, 'basic', 'import', 'a.py'),
            join(APPINSPECT_TEST_PACKAGES_PATH, 'basic', 'import', 'b.py'),
        ]
    )
])
def test_add_folder(folderpath, expected_files_added):
    dep_mgr = FileDepManager()
    dep_mgr.add_folder(folderpath)
    for expected_file_added in expected_files_added:
        assert expected_file_added in dep_mgr._file_pool


@pytest.mark.parametrize("test_package_path,expected_error_files", [
    (
        join(APPINSPECT_TEST_PACKAGES_PATH, 'syntax_error'),
        [
            join(APPINSPECT_TEST_PACKAGES_PATH, 'syntax_error', 'c.py'),
        ]
    )
])
def test_sytax_error_file_handling(test_package_path, expected_error_files):
    dep_mgr = FileDepManager()
    dep_mgr.add_folder(test_package_path)
    error_files = dep_mgr.get_syntax_error_files()
    for expected_error_file in expected_error_files:
        assert expected_error_file in error_files


@pytest.mark.parametrize("test_package_path,expected_comps", [
        (
            join(APPINSPECT_TEST_PACKAGES_PATH, 'circular_dependency', 'case1'),
            [set(["a.py", "b.py", "c.py"])]
        ),
        (
            join(APPINSPECT_TEST_PACKAGES_PATH, 'circular_dependency', 'case2'),
            [set(["a.py", "b.py", "c.py"])]
        ),
        (
            join(APPINSPECT_TEST_PACKAGES_PATH, 'circular_dependency', 'case3'),
            [set(["a.py", "b.py", "c.py"]), set(["d.py", "e.py"])]
        ),
        (
            join(APPINSPECT_TEST_PACKAGES_PATH, 'circular_dependency', 'case5'),
            [set(["a.py", "b.py", "c.py"])]
        )]
    )
def test_circular_dependency_is_detected_correctly(test_package_path, expected_comps):
    def _get_basename(comps):
        res = []
        for comp in comps:
            tmp = set()
            for path in comp:
                tmp.add(basename(path))
            res.append(tmp)
        return res
    dep_mgr = FileDepManager()
    dep_mgr.add_folder(test_package_path)
    comps = dep_mgr.get_circular_dependency()
    comps = _get_basename(comps)
    assert _verify_comps(comps, expected_comps)


@pytest.mark.parametrize("test_package_path,expected_loops_collection", [
        (
            join(APPINSPECT_TEST_PACKAGES_PATH, 'circular_dependency', 'case1'),
            [set([(("a.py", 1), ("c.py", 1), ("b.py", 1))])]
        ),
        (
            join(APPINSPECT_TEST_PACKAGES_PATH, 'circular_dependency', 'case2'),
            [set([(("a.py", 1), ("c.py", 1), ("b.py", 2)), (("a.py", 1), ("b.py", 1)), (("a.py", 2), ("c.py", 1))])]
        ),
        (
            join(APPINSPECT_TEST_PACKAGES_PATH, 'circular_dependency', 'case5'),
            [set([(("a.py", 1), ("b.py", 1)), (("b.py", 2), ("c.py", 1))])]
        )]
    )
def test_circular_dependency_loop_is_detected_correctly(test_package_path, expected_loops_collection):
    def _get_basename(comps):
        res = []
        for comp in comps:
            tmp = []
            for tup in comp:
                path = tup[0]
                tmp.append((basename(path), tup[1]))
            res.append(tuple(tmp))
        return set(res)
    dep_mgr = FileDepManager()
    dep_mgr.add_folder(test_package_path)
    loops_collection = dep_mgr.find_circular_dependency_loops()
    procd_loops_collection = []
    for loops in loops_collection:
        basename_loops = _get_basename(loops)
        procd_loops_collection.append(basename_loops)
    assert procd_loops_collection == expected_loops_collection


@pytest.mark.parametrize("test_package_path,rules", [
        (
            join(APPINSPECT_TEST_PACKAGES_PATH, 'basic', 'import'),
            [("a.py", "b.py")]
        ),
        (
            join(APPINSPECT_TEST_PACKAGES_PATH, 'basic', 'from_import'),
            [("a.py", "b.py")]
        ),
        (
            join(APPINSPECT_TEST_PACKAGES_PATH, 'basic', 'multi_children'),
            [("a.py", "c.py"), ("b.py", "c.py")]
        ),
        (
            join(APPINSPECT_TEST_PACKAGES_PATH, 'basic', 'multi_parents'),
            [("a.py", "c.py"), ("a.py", "b.py"), ("a.py", "d.py")]
        ),
        (
            join(APPINSPECT_TEST_PACKAGES_PATH, 'basic', 'multi_items', 'import'),
            [("a.py", "b.py"), ("a.py", "c.py")]
        ),
        (
            join(APPINSPECT_TEST_PACKAGES_PATH, 'basic', 'multi_items', 'from_import'),
            [("a.py", "b.py")]
        )]
    )
def test_files_are_iterated_in_topological_order_in_basic_scenarios(test_package_path, rules):
    # Test basic/import
    dep_mgr = FileDepManager()
    dep_mgr.add_folder(test_package_path)
    target = [basename(file) for file in dep_mgr.iter_files()]
    assert _verify_iteration_order(target, rules)



@pytest.mark.parametrize("test_package_path,rules", [
    (
        join(APPINSPECT_TEST_PACKAGES_PATH, 'complicated_topology', 'triangle'),
        [
            ("a.py", "b.py"),
            ("a.py", "c.py"),
            ("b.py", "c.py"),
        ]
    ),
    (
        join(APPINSPECT_TEST_PACKAGES_PATH, 'complicated_topology', 'rectangle'),
        [
            ("a.py", "b.py"),
            ("a.py", "c.py"),
            ("a.py", "d.py"),
            ("b.py", "c.py"),
            ("b.py", "d.py"),
            ("c.py", "d.py"),
        ]
    ),
])
def test_files_are_iterated_in_topological_order_in_complicated_scenarios(test_package_path, rules):
    # Test complicated_topology/triangle
    dep_mgr = FileDepManager()
    dep_mgr.add_folder(test_package_path)
    target = [basename(file) for file in dep_mgr.iter_files()]
    assert _verify_iteration_order(target, rules)


@pytest.mark.parametrize("test_package_path,expected_dependency", [
    (
        join(APPINSPECT_TEST_PACKAGES_PATH, 'basic', 'import', 'a.py'),
        {
            'filepath': join(APPINSPECT_TEST_PACKAGES_PATH, 'basic', 'import', 'a.py'),
            'parents': [
                {
                    'filepath': join(APPINSPECT_TEST_PACKAGES_PATH, 'basic', 'import', 'b.py'),
                    'parents': []
                }
            ]
        }
    )
])
def test_get_dependency(test_package_path, expected_dependency):
    dep_mgr = FileDepManager()
    dep_mgr.add_file(test_package_path)
    assert dep_mgr.get_dependences(test_package_path) == expected_dependency


def test_get_error_files():
    dep_manager = FileDepManager()
    dep_manager.add_folder(join(APPINSPECT_TEST_PACKAGES_PATH, 'multi_errors'))

    syntax_error_files = dep_manager.get_syntax_error_files()
    null_byte_error_files = dep_manager.get_null_byte_error_files()
    other_exception_files = dep_manager.get_other_exception_files()

    syntax_error_files = list(map(basename, syntax_error_files))
    null_byte_error_files = list(map(basename, null_byte_error_files))
    other_exception_files = list(map(basename, other_exception_files))

    assert syntax_error_files == ['syntax_error.py']
    assert null_byte_error_files == ['null_byte_error.py']
    assert other_exception_files == []

def test_syntax_error_files_wont_be_linked_with_other():
    dep_manager = FileDepManager()
    dep_manager.add_folder(join(APPINSPECT_TEST_PACKAGES_PATH, 'multi_errors'))

    normal_files = []
    for filepath in dep_manager.iter_files():
        normal_files.append(basename(filepath))
    assert normal_files == ['normal_file.py']


def test_get_hidden_files():

    app_dir = join(APPINSPECT_TEST_PACKAGES_PATH, "hidden_python_files")
    temp_dir = join(tempfile.mkdtemp(), "tmp")
    shutil.copytree(app_dir, temp_dir)

    dep_manager = FileDepManager()
    dep_manager.add_folder(temp_dir)

    shutil.rmtree(dirname(temp_dir))

    # real python files would be included in dependency graph
    paths = sorted([filepath for filepath in dep_manager.iter_files()])
    assert paths == [join(temp_dir, 'a.py'),
                     join(temp_dir, 'hidden_python')]

    # other files would be included in hidden python files
    hidden_paths = sorted([filepath for filepath in dep_manager.get_hidden_python_files()])
    syntax_paths = sorted([filepath for filepath in dep_manager.get_syntax_error_files()])
    assert hidden_paths == [join(temp_dir, 'template.html')]
    assert syntax_paths == []


def test_nodes_connect_to_circular_dependency():
    """
             a    -  f
               \
           |    b
              /
           c
           |
           d
           |
           e

        edges:
        b -> a
        c -> b
        a -> c
        c -> d
        d -> e
        f -> a

        so (a,b,c) is a SCC
    """
    app_dir = join(APPINSPECT_TEST_PACKAGES_PATH, "nodes_connect_to_circular_dependency")

    dep_manager = FileDepManager()
    dep_manager.add_folder(app_dir)

    assert sorted([filepath for filepath in dep_manager.iter_circular_dependency_files()]) == \
           [join(app_dir, "a.py"), join(app_dir, "b.py"), join(app_dir, "c.py")]
    assert sorted([filepath for filepath in dep_manager.iter_non_circular_dependency_files()]) == \
           [join(app_dir, "d.py"), join(app_dir, "e.py"), join(app_dir, "f.py")]
    assert sorted([filepath for filepath in dep_manager.iter_files()]) == \
           [join(app_dir, "a.py"), join(app_dir, "b.py"), join(app_dir, "c.py"),
            join(app_dir, "d.py"), join(app_dir, "e.py"), join(app_dir, "f.py")]


def test_ssc_with_a_bridge_node():
    app_dir = join(APPINSPECT_TEST_PACKAGES_PATH, "two_ssc_with_a_bridge_node")

    dep_manager = FileDepManager()
    dep_manager.add_folder(app_dir)

    circular_dependency = dep_manager.get_circular_dependency()
    for loop in circular_dependency:
        loop.sort()
    circular_dependency.sort()

    assert circular_dependency[0] == [join(app_dir, "a.py"), join(app_dir, "b.py"), join(app_dir, "c.py")]
    assert circular_dependency[1] == [join(app_dir, "e.py"), join(app_dir, "f.py"), join(app_dir, "g.py")]
    assert sorted([filepath for filepath in dep_manager.iter_non_circular_dependency_files()]) == [join(app_dir, "d.py")]
    assert sorted([filepath for filepath in dep_manager.iter_files()]) == \
        [join(app_dir, "a.py"), join(app_dir, "b.py"), join(app_dir, "c.py"), join(app_dir, "d.py"),
         join(app_dir, "e.py"), join(app_dir, "f.py"), join(app_dir, "g.py")]


def test_self_loop():
    app_dir = join(APPINSPECT_TEST_PACKAGES_PATH, "self_loop")

    dep_manager = FileDepManager()
    dep_manager.add_folder(app_dir)

    assert sorted([filepath for filepath in dep_manager.iter_non_circular_dependency_files()]) == [join(app_dir, "a.py")]
    assert sorted([filepath for filepath in dep_manager.iter_circular_dependency_files()]) == []
    assert sorted([filepath for filepath in dep_manager.iter_files()]) == [join(app_dir, "a.py")]


def test_preprocess_functionality():
    file_dir = join(APPINSPECT_TEST_PACKAGES_PATH, "inconsistent_tab_space")
    dep_manager = FileDepManager()
    if six.PY3:
        for fi in os.listdir(file_dir):
            if fi.endswith('.py'):
                try:
                    shutil.copy(join(file_dir, fi), join(file_dir, fi + '.test'))

                    with pytest.raises(TabError):
                        ast.parse(open(join(file_dir, fi + '.test')).read())

                    dep_manager._preprocess_file(join(file_dir, fi + '.test'))
                    ast.parse(open(join(file_dir, fi + '.test')).read())
                except:
                    raise
                finally:
                    if os.path.isfile(join(file_dir, fi + '.test')):
                        os.remove(join(file_dir, fi + '.test'))
                    if os.path.isfile(join(file_dir, fi + '.test.raw')):
                        os.remove(join(file_dir, fi + '.test.raw'))
    else:
        for fi in os.listdir(file_dir):
            if fi.endswith('.py'):
                ast.parse(open(join(file_dir, fi)).read())