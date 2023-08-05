import os
import ast
import six

from collections import deque

from splunk_appinspect.python_modules_metadata.python_modules_metadata_store import metadata_store
from splunk_appinspect.python_modules_metadata.metadata_common import metadata_consts
from splunk_appinspect.python_modules_metadata.metadata_common import metadata_types

from splunk_appinspect.python_modules_metadata.metadata_common.metadata_exceptions import EmptyNamespace, \
    IllegalAsteriskNamespace

from enum import Enum


def test_basic_functionality():
    query = metadata_store.query()
    modules = query.name('os').namespace_prefix('os').modules()
    assert len(modules) == 1
    assert isinstance(modules[0], metadata_types.ModuleMetadata)
    assert modules[0].name == 'os'
    assert modules[0].namespace == 'os'


'''
    Use this bunch of test cases to ensure we add new modules, functions, classes, attributes correctly
'''


def test_root_module_property():
    root_module = metadata_store.root_module
    assert isinstance(root_module, metadata_types.ModuleMetadata)
    assert root_module.functions == []
    assert root_module.classes == []
    assert root_module.name == 'metadata'
    assert len(root_module.sub_modules) > 0


def test_total_number_of_modules():
    # use this test case to ensure we add new modules correctly
    query = metadata_store.query()
    modules = query.modules()
    assert len(modules) > 0


def test_total_number_of_functions():
    # use this test case to ensure we add new functions correctly
    query = metadata_store.query()
    functions = query.functions()
    assert len(functions) > 0


def test_total_number_of_classes():
    # use this test cases to ensure we add new classes correctly
    query = metadata_store.query()
    classes = query.classes()
    assert len(classes) > 0


def test_total_number_of_components():
    query = metadata_store.query()
    all_components = query.collect()

    query.reset()
    all_functions = query.functions()

    query.reset()
    all_classes = query.classes()

    query.reset()
    all_modules = query.modules()

    assert len(all_components) == len(all_modules) + len(all_functions) + len(all_classes)


def test_create_isolated_query():
    query1 = metadata_store.query()
    query2 = metadata_store.query()
    assert id(query1) != id(query2)


def test_filter_by_name():
    query = metadata_store.query()
    modules = query.name(metadata_consts.ModuleNameConsts.OS).modules()
    assert len(modules) == 1

    query = metadata_store.query()
    modules = query.name('rmtree').collect()
    assert len(modules) == 1


def test_filter_by_namespace_prefix():
    query = metadata_store.query()
    functions = query.namespace_prefix(metadata_consts.ModuleNameConsts.OS).functions()
    assert len(functions) == 45

    query.reset()
    modules = query.namespace_prefix(metadata_consts.ModuleNameConsts.OS).modules()
    assert len(modules) == 2


def test_filter_by_namespace_prefix_with_same_prefix_in_string():
    query = metadata_store.query()
    # urllib is urllib2's prefix in string, but not in namespace

    query.reset()
    functions1 = query.namespace_prefix(metadata_consts.ModuleNameConsts.URLLIB).functions()

    query.reset()
    functions2 = query.namespace_prefix(metadata_consts.ModuleNameConsts.URLLIB2).functions()

    assert len(functions1) == 16
    assert len(functions2) == 1

    assert len(set(functions1) & set(functions2)) == 0


def test_filter_with_complicated_prefix():
    query = metadata_store.query()

    functions = query.namespace_prefix('os.path').functions()
    assert len(functions) == 1
    assert functions[0].name == 'join'

    query.reset()
    assert len(query.namespace_prefix('o').functions()) == 0

    query.reset()
    assert len(query.namespace_prefix('os.pa').functions()) == 0

    query.reset()
    assert len(query.namespace_prefix('os.path.join.x').functions()) == 0

    query.reset()
    functions = query.namespace_prefix('os.path.join').functions()
    assert len(functions) == 1
    assert functions[0].name == 'join'


def test_filter_by_tag():
    query = metadata_store.query()
    functions = query.tag(metadata_consts.TagConsts.FILE_READ_AND_WRITE).functions()

    query.reset()
    classes = query.tag(metadata_consts.TagConsts.FILE_READ_AND_WRITE).classes()

    query.reset()
    # now modules and classes will be also be included
    objects = query.tag(metadata_consts.TagConsts.FILE_READ_AND_WRITE).collect()
    assert len(functions) + len(classes) == len(objects)


def test_filter_by_tag_and_name():
    query = metadata_store.query()
    objects = query.tag(metadata_consts.TagConsts.FILE_READ_AND_WRITE) \
        .name('mkdir') \
        .namespace_prefix(metadata_consts.ModuleNameConsts.OS).collect()
    # now macpath.os will be filtered, since namespace_prefix is used
    assert len(objects) == 1
    assert objects[0].name == 'mkdir'
    assert objects[0].namespace == 'os.mkdir'
    assert isinstance(objects[0], metadata_types.FunctionMetadata)


def test_filter_by_names():
    query = metadata_store.query()
    objects = query.names([metadata_consts.ModuleNameConsts.SHUTIL, metadata_consts.ModuleNameConsts.CSV]).modules()
    assert len(objects) == 2
    assert isinstance(objects[0], metadata_types.ModuleMetadata)
    assert isinstance(objects[1], metadata_types.ModuleMetadata)


def test_find_all_file_manipulation_functions_in_different_constraints():
    query = metadata_store.query()
    objects = query.tag(metadata_consts.TagConsts.FILE_READ_AND_WRITE) \
        .namespace_prefix(metadata_consts.ModuleNameConsts.OS).functions()
    assert len(objects) == 40

    query = metadata_store.query()
    objects = query.tag(metadata_consts.TagConsts.FILE_READ_AND_WRITE) \
        .namespace_prefixes([metadata_consts.ModuleNameConsts.OS, metadata_consts.ModuleNameConsts.SHUTIL]) \
        .functions()
    assert len(objects) == 53

    query = metadata_store.query()
    objects = query.tag(metadata_consts.TagConsts.FILE_READ_AND_WRITE) \
        .namespace_prefix('what') \
        .functions()
    assert len(objects) == 0


def test_reset_query():
    query = metadata_store.query()
    modules = query.name(metadata_consts.ModuleNameConsts.TEMPFILE).modules()
    assert len(modules) == 1
    assert modules[0].name == 'tempfile'

    # without reset, previous filter conditions won't be invalidated
    functions = query.namespace_prefix('os').functions()
    assert len(functions) == 0

    query.reset()
    # now query result is correct
    functions = query.namespace_prefix('os').functions()
    assert len(functions) == 45


def test_check_for_files_and_directories_access_scenario():
    # find all sensitive usage tagged with FILE_AND_DIRECTORY_ACCESS
    query = metadata_store.query()

    modules = [metadata_consts.ModuleNameConsts.OS, metadata_consts.ModuleNameConsts.SHUTIL,
               metadata_consts.ModuleNameConsts.TEMPFILE, metadata_consts.ModuleNameConsts.LINECACHE]
    functions = query.namespace_prefixes(modules).tag(metadata_consts.TagConsts.FILE_READ_AND_WRITE).functions()
    assert len(functions) == 64

    modules = query.namespace_prefixes(modules).tag(metadata_consts.TagConsts.FILE_READ_AND_WRITE).modules()
    assert len(modules) == 0

    classes = query.namespace_prefixes(modules).tag(metadata_consts.TagConsts.FILE_READ_AND_WRITE).classes()
    assert len(classes) == 1


def test_class_inheritance_scenario():
    query = metadata_store.query()

    classes = query.name('ConfigParser').classes()
    assert len(classes) == 2

    # choose python2 metadata
    config_parser = classes[0] if classes[0].namespace == 'ConfigParser.ConfigParser' else classes[1]
    assert config_parser.namespace == 'ConfigParser.ConfigParser'

    assert len(config_parser.functions) == 3

    functions = config_parser.functions
    functions.sort(key=lambda func: func.name)

    assert functions[0].name == 'read'
    assert functions[1].name == 'readfp'
    assert functions[2].name == 'write'

    for func in functions:
        assert func.tags == {metadata_consts.TagConsts.FILE_READ_AND_WRITE, metadata_consts.TagConsts.PY2_ONLY}


def test_all_functions_are_tagged():
    '''
        All functions should be tagged, since all functions listed in metadata should be sensitive
        Some classes could be ignored
    '''
    query = metadata_store.query()
    for obj in query.functions():
        assert len(obj.tags) > 0, 'function {} has no tags, please add corresponding tags to this function'.format(
            obj.namespace)


def test_all_components_are_described():
    query = metadata_store.query()
    for obj in query.collect():
        # all component need to be described
        assert obj.description != '', 'Component {} is not described, please add description string for it'.format(
            obj.namespace)


def test_use_tag_to_filter_modules():
    query = metadata_store.query().tag(metadata_consts.TagConsts.CRITICAL_SYSTEM_MODULE)
    modules = query.modules()
    modules.sort(key=lambda node: node.name)
    names = list(map(lambda node: node.name, modules))
    assert names == ['os', 'socket']

    query.reset()
    modules = query.tag(metadata_consts.TagConsts.FILE_READ_AND_WRITE).modules()
    assert len(modules) == 0


def test_multi_tags_filter():
    query = metadata_store.query().tag(metadata_consts.TagConsts.CRITICAL_SYSTEM_MODULE) \
        .tag(metadata_consts.TagConsts.XML_RPC_CONNECTION)
    components = query.collect()
    assert len(components) == 4


def test_filter_by_tags():
    query = metadata_store.query().tags(
        [metadata_consts.TagConsts.CRITICAL_SYSTEM_MODULE, metadata_consts.TagConsts.XML_RPC_CONNECTION])
    components = query.collect()
    assert len(components) == 4


def test_component_attributes():
    # use shutil.rmtree as example
    query = metadata_store.query().name('rmtree')
    objects = query.collect()

    assert len(objects) == 1
    func = objects[0]

    assert func.name == 'rmtree'
    assert func.namespace == 'shutil.rmtree'
    assert func.tags == {metadata_consts.TagConsts.FILE_READ_AND_WRITE}
    assert func.description == 'remove files/directories'


def test_nested_module():
    # os.path
    query = metadata_store.query().name('path').namespace_prefix('os')
    modules = query.modules()
    assert len(modules) == 1

    module = modules[0]
    assert module.name == 'path'
    assert module.namespace == 'os.path'
    assert module.description == 'path manipulation'
    assert len(module.functions) == 1

    func = module.functions[0]
    assert func.name == 'join'
    assert func.namespace == 'os.path.join'
    assert func.description == 'join arguments'


def test_total_number_of_modules_based_on_files():
    project_root_path = os.path.abspath(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
    modules_root_path = os.path.join(project_root_path, 'splunk_appinspect', 'python_modules_metadata', 'metadata')

    query = metadata_store.query()

    total_modules = 0
    for _, dirs, files in os.walk(modules_root_path):
        for f in files:
            if f.endswith('.py'):
                total_modules += 1

    # __init__.py in metadata directory should be excluded
    assert len(query.modules()) == total_modules - 1


'''
Since class inheritance is allowed, we can not use ast.FunctionDef to determine how many functions 
in out metadata store 

Test case like `test_total_number_of_functions_based_on_files` is not available now
'''


def test_total_number_of_classes_based_on_files():
    # unit -> test -> appinspect
    project_root_path = os.path.abspath(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
    modules_root_path = os.path.join(project_root_path, 'splunk_appinspect', 'python_modules_metadata', 'metadata')

    query = metadata_store.query()

    total_classes = 0
    for root, dirs, files in os.walk(modules_root_path):
        for f in files:
            python_file_path = os.path.join(root, f)
            if f.endswith('.py'):
                ast_tree = ast.parse(open(python_file_path).read())
                for node in ast.walk(ast_tree):
                    if isinstance(node, ast.ClassDef):
                        total_classes += 1

    assert len(query.classes()) == total_classes


def test_multi_namespace_and_specified_tag():
    query = metadata_store.query()

    total_functions = set(query.tag(metadata_consts.TagConsts.FILE_READ_AND_WRITE) \
                          .namespace_prefix(metadata_consts.ModuleNameConsts.SHUTIL) \
                          .namespace_prefix(metadata_consts.ModuleNameConsts.OS).functions())

    query.reset()
    shutil_functions = set(query.tag(metadata_consts.TagConsts.FILE_READ_AND_WRITE) \
                           .namespace_prefix(metadata_consts.ModuleNameConsts.SHUTIL).functions())

    query.reset()
    os_functions = set(query.tag(metadata_consts.TagConsts.FILE_READ_AND_WRITE) \
                       .namespace_prefix(metadata_consts.ModuleNameConsts.OS).functions())

    assert total_functions == shutil_functions | os_functions


def test_multi_namespaces_and_multi_tags():
    query = metadata_store.query()

    total_functions = set(query.namespace_prefix(metadata_consts.ModuleNameConsts.SHUTIL) \
                          .namespace_prefix(metadata_consts.ModuleNameConsts.REQUESTS) \
                          .tag(metadata_consts.TagConsts.FILE_READ_AND_WRITE) \
                          .tag(metadata_consts.TagConsts.HTTP_CONNECTION).functions())

    query.reset()
    shutil_with_file_read_and_write_tag = set(query.tag(metadata_consts.TagConsts.FILE_READ_AND_WRITE) \
                                              .namespace_prefix(metadata_consts.ModuleNameConsts.SHUTIL).functions())

    query.reset()
    requests_with_http_connection_tag = set(query.tag(metadata_consts.TagConsts.HTTP_CONNECTION) \
                                            .namespace_prefix(metadata_consts.ModuleNameConsts.REQUESTS).functions())

    assert total_functions == shutil_with_file_read_and_write_tag | requests_with_http_connection_tag


def test_all_components_are_unique():
    '''
    Sometimes we define some duplicate functions or classes by mistake, use this test cases to
    guarantee all functions, classes are unique
    '''
    # unit -> test -> appinspect
    project_root_path = os.path.abspath(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
    modules_root_path = os.path.join(project_root_path, 'splunk_appinspect', 'python_modules_metadata', 'metadata')

    for root, dirs, files in os.walk(modules_root_path):
        for f in files:
            path = os.path.join(root, f)
            if path.endswith('.py'):
                namespace_set = set()
                ast_root = ast.parse(open(path, 'r').read())
                queue = deque()
                queue.append((ast_root, ''))
                while queue:
                    current_node, namespace = queue.popleft()
                    # only check Function node and Class node
                    if isinstance(current_node, (ast.FunctionDef, ast.ClassDef)):
                        namespace = current_node.name if namespace == '' else namespace + '.' + current_node.name
                        assert namespace not in namespace_set, 'Duplicate {} component defined in metadata store'.format(
                            namespace)
                        namespace_set.add(namespace)
                    for child_node in ast.iter_child_nodes(current_node):
                        queue.append((child_node, namespace))


def test_all_tags_are_used():
    tags_used, tags_defined = set(), set()
    for component in metadata_store.query().collect():
        tags_used |= component.tags
    # collect all tags in metadata_consts
    for attr in dir(metadata_consts.TagConsts):
        attribute = getattr(metadata_consts.TagConsts, attr)
        if isinstance(attribute, Enum):
            tags_defined.add(attribute)
    assert tags_used == tags_defined, \
        'tags {} defined but not used anywhere, please double check if you need these tags'.format(
            str(tags_defined - tags_used))


def test_exclude_namespace_prefix():
    query = metadata_store.query()
    # exclude os namespace
    functions = query.exclude_namespace_prefix(metadata_consts.ModuleNameConsts.OS).functions()

    query.reset()
    # include os namespace
    os_functions = query.namespace_prefix(metadata_consts.ModuleNameConsts.OS).functions()

    query.reset()
    assert len(functions) == len(query.functions()) - len(os_functions)

    for function in functions:
        assert not function.namespace.startswith(metadata_consts.ModuleNameConsts.OS.value)


def test_exclude_namespace_prefixes():
    # Use different APIs
    query = metadata_store.query()
    functions1 = query.exclude_namespace_prefixes(
        [metadata_consts.ModuleNameConsts.OS, metadata_consts.ModuleNameConsts.SHUTIL]) \
        .functions()

    query.reset()
    functions2 = query.exclude_namespace_prefix(metadata_consts.ModuleNameConsts.OS).exclude_namespace_prefix(
        metadata_consts.ModuleNameConsts.SHUTIL) \
        .functions()

    assert functions1 == functions2


def test_exclude_tag():
    query = metadata_store.query()
    functions1 = query.exclude_tag(metadata_consts.TagConsts.HTTP_CONNECTION).functions()
    for function in functions1:
        assert not function.namespace.startswith(metadata_consts.TagConsts.HTTP_CONNECTION.value)

    query.reset()
    functions2 = query.tag(metadata_consts.TagConsts.HTTP_CONNECTION).functions()

    query.reset()
    assert len(functions2) == len(query.functions()) - len(functions1)

    query.reset()
    assert len(query.functions()) == len(functions1) + len(functions2)
    assert set(query.functions()) == set(functions1) | set(functions2)


def test_exclude_tags():
    query = metadata_store.query().exclude_tag(metadata_consts.TagConsts.FILE_READ_AND_WRITE) \
        .exclude_tag(metadata_consts.TagConsts.HTTP_CONNECTION)
    functions1 = query.functions()

    query.reset()
    functions2 = query.exclude_tags(
        [metadata_consts.TagConsts.HTTP_CONNECTION, metadata_consts.TagConsts.FILE_READ_AND_WRITE]) \
        .functions()

    assert functions1 == functions2


def test_exclude_name():
    query = metadata_store.query().exclude_name(metadata_consts.ModuleNameConsts.OS)
    modules = query.modules()

    query.reset()
    assert len(modules) == len(query.modules()) - 1


def test_exclude_names():
    query = metadata_store.query().exclude_name(metadata_consts.ModuleNameConsts.OS) \
        .exclude_name(metadata_consts.ModuleNameConsts.SHUTIL)
    modules = query.modules()

    query.reset()
    assert len(modules) == len(query.modules()) - 2


def test_mix_include_and_exclude():
    query = metadata_store.query()

    query.exclude_namespace_prefix(metadata_consts.ModuleNameConsts.OS) \
        .exclude_namespace_prefix(metadata_consts.ModuleNameConsts.TEMPFILE) \
        .namespace_prefix(metadata_consts.ModuleNameConsts.SHUTIL) \
        .namespace_prefix(metadata_consts.ModuleNameConsts.URLLIB) \
        .tag(metadata_consts.TagConsts.FILE_READ_AND_WRITE) \
        .tag(metadata_consts.TagConsts.PATH_MANIPULATION) \
        .exclude_tag(metadata_consts.TagConsts.HTTP_CONNECTION)

    # all shutil functions collected
    functions = query.functions()

    for function in functions:
        assert function.namespace.startswith(metadata_consts.ModuleNameConsts.SHUTIL.value)


def test_include_and_exclude_real_scenario():
    # find all http functions, but not include requests library
    query = metadata_store.query()

    query.tag(metadata_consts.TagConsts.HTTP_CONNECTION) \
        .exclude_namespace_prefix(metadata_consts.ModuleNameConsts.REQUESTS)

    functions = query.functions()

    # urllib, urllib2 will be collected
    query.reset()
    urllib_functions = query.namespace_prefix(metadata_consts.ModuleNameConsts.URLLIB).functions()

    query.reset()
    urllib2_functions = query.namespace_prefix(metadata_consts.ModuleNameConsts.URLLIB2).functions()

    assert len(functions) == len(urllib_functions) + len(urllib2_functions)
    assert set(functions) == set(urllib_functions) | set(urllib2_functions)


def test_include_and_exclude_same_tag():
    query = metadata_store.query()

    # we need to guarantee we use a non-empty tag
    query.tag(metadata_consts.TagConsts.HTTP_CONNECTION)
    assert len(query.collect()) > 0

    # has no effect
    query.reset()
    query.tag(metadata_consts.TagConsts.HTTP_CONNECTION) \
        .exclude_tag(metadata_consts.TagConsts.HTTP_CONNECTION)

    assert len(query.collect()) == 0


def test_namespace_module_query():
    modules = metadata_store.query_namespace('os')
    assert len(modules) == 1
    assert modules[0].name == 'os'
    assert isinstance(modules[0], metadata_types.ModuleMetadata)


def test_namespace_module_query_without_available_functions():
    modules = metadata_store.query_namespace('shutil')
    assert len(modules) == 1
    assert modules[0].name == 'shutil'

    ast_module = modules[0].instantiate()
    assert ast_module.global_map == {}


def test_namespace_module_query_with_available_functions():
    modules = metadata_store.query_namespace('os.path')
    assert len(modules) == 1
    assert modules[0].name == 'path'

    ast_module = modules[0].instantiate()
    assert 'join' in ast_module.global_map
    assert len(ast_module.global_map) == 1


def test_namespace_executable_function_query():
    functions = metadata_store.query_namespace('os.path.join')
    assert len(functions) == 1
    assert functions[0].name == 'join'
    assert functions[0].namespace == 'os.path.join'
    assert isinstance(functions[0], metadata_types.FunctionMetadata)
    assert functions[0].instantiate() is not None


def test_namespace_non_executable_function_query():
    functions = metadata_store.query_namespace('shutil.rmtree')
    assert len(functions) == 0


def test_namespace_class_query():
    classes = metadata_store.query_namespace('ConfigParser.ConfigParser')
    assert len(classes) == 1
    assert classes[0].name == 'ConfigParser'
    assert classes[0].namespace == 'ConfigParser.ConfigParser'
    assert isinstance(classes[0], metadata_types.ClassMetadata)


def test_not_exists_namespace_query():
    objects = metadata_store.query_namespace('os.path.abc')
    assert objects == []


def test_very_long_namespace():
    objects = metadata_store.query_namespace('os.path.a.d.e.f.g.h')
    assert objects == []


def test_empty_string_in_namespace():
    objects = metadata_store.query_namespace('os..path.join')
    assert objects == []


def test_namespace_module_asterisk_query():
    objects = metadata_store.query_namespace('os.*')
    assert len(objects) == 1
    modules = list(filter(lambda obj: isinstance(obj, metadata_types.ModuleMetadata), objects))
    functions = list(filter(lambda obj: isinstance(obj, metadata_types.FunctionMetadata), objects))

    assert len(modules) == 1
    assert len(functions) == 0

    assert modules[0].namespace == 'os.path'

    functions = metadata_store.query_namespace('os.path.*')
    assert len(functions) == 1
    assert isinstance(functions[0], metadata_types.FunctionMetadata)
    assert functions[0].namespace == 'os.path.join'


def test_empty_namespace_query():
    try:
        metadata_store.query_namespace('')
        assert False
    except Exception as e:
        assert isinstance(e, EmptyNamespace)


def test_asterisk_in_the_middle():
    try:
        metadata_store.query_namespace('os.*.a')
        assert False
    except Exception as e:
        assert isinstance(e, IllegalAsteriskNamespace)


def test_namespace_starts_with_asterisk():
    try:
        metadata_store.query_namespace('*.path.join')
        assert False
    except Exception as e:
        assert isinstance(e, IllegalAsteriskNamespace)


def test_namespace_with_only_one_asterisk():
    try:
        metadata_store.query_namespace('*')
        assert False
    except Exception as e:
        assert isinstance(e, IllegalAsteriskNamespace)


def test_namespace_contains_more_than_one_asterisk():
    try:
        metadata_store.query_namespace('a.*.b.*')
        assert False
    except Exception as e:
        assert isinstance(e, IllegalAsteriskNamespace)


def test_asterisk_namespace_without_executable_functions():
    modules = metadata_store.query_namespace('os.*')
    assert len(modules) == 1
    assert modules[0].name == 'path'
    assert isinstance(modules[0], metadata_types.ModuleMetadata)


def test_asterisk_namespace_with_executable_functions():
    functions = metadata_store.query_namespace('os.path.*')
    assert len(functions) == 1
    assert functions[0].name == 'join'
    assert hasattr(functions[0].python_object, 'executable')


def test_filter_with_tag_group():
    objects = metadata_store.query() \
        .tag_group([metadata_consts.TagConsts.NETWORK_CONNECTION, metadata_consts.TagConsts.CRITICAL_SYSTEM_MODULE]) \
        .collect()
    assert len(objects) == 1
    assert isinstance(objects[0], metadata_types.ModuleMetadata)
    assert objects[0].name == 'socket'

    objects = metadata_store.query() \
        .tag_group([metadata_consts.TagConsts.CRITICAL_SYSTEM_MODULE, metadata_consts.TagConsts.FILE_READ_AND_WRITE]) \
        .collect()
    assert len(objects) == 0


def test_py_version_filter():
    if six.PY2:
        classes = metadata_store.query().name("ConfigParser").python_compatible().classes()
        assert len(classes) == 1
        config_parser_class = classes[0]
        assert config_parser_class.namespace == "ConfigParser.ConfigParser"
    else:
        classes = metadata_store.query().name("ConfigParser").python_compatible().classes()
        assert len(classes) == 2
        class_names = {classes[0].namespace, classes[1].namespace}
        assert class_names == {"ConfigParser.ConfigParser", "configparser.ConfigParser"}


def test_py2_exclusive_class_filter():
    classes = metadata_store.query().namespace_prefix("ConfigParser.ConfigParser").python_compatible().classes()
    assert len(classes) == 1
    assert classes[0].tags == {metadata_consts.TagConsts.PY2_ONLY}


def test_py3_exclusive_function_filter():
    functions = metadata_store.query().namespace_prefix("dbm.gnu").name("open").python_compatible().functions()
    if six.PY2:
        assert len(functions) == 0
    else:
        assert len(functions) == 1

def test_py_compatible_module_filter():
    modules = metadata_store.query().name("os").python_compatible().modules()
    assert len(modules) == 1