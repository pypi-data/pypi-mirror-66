import os
import ast
import re
import six

from collections import deque

from splunk_appinspect.python_analyzer.ast_analyzer import AstAnalyzer
from splunk_appinspect.python_analyzer.ast_types import AstVariable, AstClass, AstFunction, AstModule, AstContext, AstCallableFunction
from splunk_appinspect.python_analyzer.ast_info_query import Any


from pympler import asizeof

TEST_PACKAGE_ROOT = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'python_analyzer_packages', 'ast_analyzer_python_files')


def test_simple_python_file_parse():

    error_exists = False
    try:
        if six.PY2:
            AstAnalyzer(python_file_path=os.path.join(TEST_PACKAGE_ROOT, 'simple_python_file_ACD-2725_py2.py'))
        else:
            AstAnalyzer(python_file_path=os.path.join(TEST_PACKAGE_ROOT, 'simple_python_file_ACD-2725_py3.py'))
    except:
        error_exists = True
    assert error_exists == False


def test_parse_python_file_with_consecutive_enter_characters():

    analyzer = AstAnalyzer(python_file_path=os.path.join(TEST_PACKAGE_ROOT, 'modalert_opswat_ai_helper.py'))
    lines = analyzer.python_code_lines
    # \r\r\n won't be merged into \n
    assert len(lines) == 122
    assert lines[0] == '# encoding = utf-8'
    assert lines[1] == ''
    assert lines[2] == 'def query_url(helper, hashvalue, apikey, request_timeout_rate, themethod):'


def test_complicated_python_file_parse():

    error_exists = False
    try:
        if six.PY2:
            AstAnalyzer(python_file_path=os.path.join(TEST_PACKAGE_ROOT, 'complicated_python_file_ACD-2725_py2.py'))
        else:
            AstAnalyzer(python_file_path=os.path.join(TEST_PACKAGE_ROOT, 'complicated_python_file_ACD-2725_py3.py'))
    except:
        error_exists = True
    assert error_exists == False


def test_very_huge_python_file_parse():

    error_exists = False
    try:
        if six.PY2:
            AstAnalyzer(python_file_path=os.path.join(TEST_PACKAGE_ROOT, 'very_huge_python_file_ACD-2725_py2.py'))
        else:
            AstAnalyzer(python_file_path=os.path.join(TEST_PACKAGE_ROOT, 'very_huge_python_file_ACD-2725_py3.py'))
    except:
        error_exists = True
    assert error_exists == False


def test_parse_illegal_python_file():

    # illegal python code string
    code_string = 'def func() pass'
    try:
        AstAnalyzer(python_code_string=code_string)
        assert False
    except Exception as e:
        assert isinstance(e, SyntaxError)

def test_root_ast_node():

    analyzer = AstAnalyzer(python_file_path=os.path.join(TEST_PACKAGE_ROOT, 'basic_root_ast_node_ACD-2725.py'))
    assert isinstance(analyzer.root_ast_node, ast.Module)


def test_python_code_lines():

    analyzer = AstAnalyzer(python_file_path=os.path.join(TEST_PACKAGE_ROOT, 'basic_python_code_lines_ACD-2725.py'))
    code_lines = analyzer.python_code_lines
    assert len(code_lines) == 3

    assert code_lines[0] == 'import os'
    assert code_lines[1] == ''
    assert code_lines[2] == 'a = 10'


def test_module_manager_property():

    class ModuleManager:
        def load_modules(self):
            return ['for test']

    analyzer = AstAnalyzer(python_code_string='a = 10', module_manager=ModuleManager())
    assert analyzer.module_manager is not None
    assert analyzer.module_manager.load_modules() == ['for test']


def test_basic_get_module_usage():

    if six.PY2:
        analyzer = AstAnalyzer(python_file_path=os.path.join(TEST_PACKAGE_ROOT, 'basic_get_module_usage_ACD-2725_py2.py'))
    else:
        analyzer = AstAnalyzer(python_file_path=os.path.join(TEST_PACKAGE_ROOT, 'basic_get_module_usage_ACD-2725_py3.py'))

    lineno_list = analyzer.get_module_usage('os', lineno_only=True)
    assert lineno_list == [1 , 3 , 4]

    nodes = analyzer.get_module_usage('os')
    assert len(nodes) == 6

    # `os` in os.path.join, `os` in print a
    assert len(list(filter(lambda node: isinstance(node, ast.Name), nodes))) == 2
    # `os.path` in os.path.join, `os.path.join` in os.path.join
    assert len(list(filter(lambda node: isinstance(node, ast.Attribute), nodes))) == 2
    # `os` in import os
    assert len(list(filter(lambda node: isinstance(node, ast.Import), nodes))) == 1
    # `os` in call node
    assert len(list(filter(lambda node: isinstance(node, ast.Call), nodes))) == 1


def test_basic_get_module_function_call_usage():

    if six.PY2:
        analyzer = AstAnalyzer(python_file_path=os.path.join(TEST_PACKAGE_ROOT, 'basic_get_module_function_call_usage_ACD-2725_py2.py'))
    else:
        analyzer = AstAnalyzer(python_file_path=os.path.join(TEST_PACKAGE_ROOT, 'basic_get_module_function_call_usage_ACD-2725_py3.py'))

    lineno_list = analyzer.get_module_function_call_usage('shutil', 'rmtree', lineno_only=True)
    assert lineno_list == [3]

    nodes = analyzer.get_module_function_call_usage('shutil', 'rmtree')
    assert len(nodes) == 1

    # get_module_function_call_usage should always return `ast.Call` node
    assert all(map(lambda node: isinstance(node, ast.Call), nodes)) == True


def test_advanced_get_module_function_call_usage_with_function_args():

    analyzer = AstAnalyzer(python_file_path=os.path.join(TEST_PACKAGE_ROOT, 'advanced_get_module_function_call_usage_ACD-2725.py'))
    # Here arg_values are plain text string
    lineno_list = analyzer.get_module_function_call_usage('socket', 'socket',
                                                          function_args={
                                                              0: {
                                                                  'arg_values': ['socket.AF_INET'],
                                                                  'required': True
                                                              },
                                                              1: {
                                                                  'arg_values': ['socket.SOCK_DGRAM'],
                                                                  'required': True
                                                              }
                                                          }, lineno_only=True)
    assert lineno_list == [3]

    lineno_list = analyzer.get_module_function_call_usage('socket', 'socket',
                                                          function_args={
                                                              0: {
                                                                  'arg_values': ['socket.AF_INET'],
                                                                  'required': True
                                                              }
                                                          }, lineno_only=True)
    assert lineno_list == [3]

    lineno_list = analyzer.get_module_function_call_usage('socket', 'socket',
                                                          function_args={
                                                              0: {
                                                                  'arg_values': ['haha'],
                                                                  'required': True
                                                              }
                                                          }, lineno_only=True)
    assert lineno_list == []


def test_basic_get_module_all_possible_usage():

    if six.PY2:
        analyzer = AstAnalyzer(python_file_path=os.path.join(TEST_PACKAGE_ROOT, 'basic_get_module_all_possible_usage_ACD-2725_py2.py'))
    else:
        analyzer = AstAnalyzer(python_file_path=os.path.join(TEST_PACKAGE_ROOT, 'basic_get_module_all_possible_usage_ACD-2725_py3.py'))

    lineno_list = analyzer.get_module_all_possible_usage('os', lineno_only=True)
    assert lineno_list == [1 , 2 , 4 , 5]

    nodes = analyzer.get_module_all_possible_usage('os')
    assert len(nodes) == 7

    assert len(list(filter(lambda node: isinstance(node, ast.Name), nodes))) == 2
    assert len(list(filter(lambda node: isinstance(node, ast.Attribute), nodes))) == 2
    # two import nodes are collected here
    assert len(list(filter(lambda node: isinstance(node, ast.Import), nodes))) == 2
    assert len(list(filter(lambda node: isinstance(node, ast.Call), nodes))) == 1


def test_basic_get_literal_string_usage():

    if six.PY2:
        analyzer = AstAnalyzer(python_file_path=os.path.join(TEST_PACKAGE_ROOT, 'basic_get_literal_string_usage_ACD-2725_py2.py'))
    else:
        analyzer = AstAnalyzer(
            python_file_path=os.path.join(TEST_PACKAGE_ROOT, 'basic_get_literal_string_usage_ACD-2725_py3.py'))

    lineno_list = analyzer.get_literal_string_usage('hello world', lineno_only=True)
    assert lineno_list == [4]

    nodes = analyzer.get_literal_string_usage('hello world')
    assert len(nodes) == 1
    assert isinstance(nodes[0], ast.BinOp)

    lineno_list = analyzer.get_literal_string_usage('Hell.*', flags=re.IGNORECASE, lineno_only=True)
    assert lineno_list == [1 , 4]

    nodes = analyzer.get_literal_string_usage('Hell.*', flags=re.IGNORECASE)
    assert len(nodes) == 5
    assert len(list(filter(lambda node: isinstance(node, ast.Str), nodes))) == 1
    assert len(list(filter(lambda node: isinstance(node, ast.BinOp), nodes))) == 2
    assert len(list(filter(lambda node: isinstance(node, ast.Name), nodes))) == 2


def test_basic_get_code_piece_usage():

    analyzer = AstAnalyzer(python_file_path=os.path.join(TEST_PACKAGE_ROOT, 'basic_get_code_piece_usage_ACD-2725.py'))
    lineno_list = analyzer.get_code_piece_usage('import os', lineno_only=True)
    assert lineno_list == [1 , 4]

    nodes = analyzer.get_code_piece_usage('import os')
    assert len(nodes) == 2
    assert len(list(filter(lambda node: isinstance(node, ast.Import), nodes))) == 2


def test_basic_get_variable_distribution():

    if six.PY2:
        analyzer = AstAnalyzer(python_file_path=os.path.join(TEST_PACKAGE_ROOT, 'basic_get_variable_distribution_ACD-2725_py2.py'))
    else:
        analyzer = AstAnalyzer(
            python_file_path=os.path.join(TEST_PACKAGE_ROOT, 'basic_get_variable_distribution_ACD-2725_py3.py'))

    lineno_list = analyzer.get_variable_distribution('value', lineno_only=True)
    assert lineno_list == [1, 3, 6]

    nodes = analyzer.get_variable_distribution('value')
    assert len(nodes) == 3
    '''
        1. value = 10
        2. b = value
        3. print value
        All value name nodes would be collected
    '''
    assert len(list(filter(lambda node: isinstance(node, ast.Name), nodes))) == 3


def test_basic_get_variable_details():

    analyzer = AstAnalyzer(python_file_path=os.path.join(TEST_PACKAGE_ROOT, 'basic_get_variable_details_ACD-2725.py'))
    ast_nodes = analyzer.get_variable_distribution('value')

    assert len(ast_nodes) == 1
    ast_node = ast_nodes[0]
    assert isinstance(ast_node, ast.Name)

    variable = analyzer.get_variable_details(ast_node)
    assert isinstance(variable, AstVariable)
    assert len(variable.variable_type_set) == 1
    assert 'os' in variable.variable_type_set


def test_basic_get_call_node_modules():

    analyzer = AstAnalyzer(python_file_path=os.path.join(TEST_PACKAGE_ROOT, 'basic_get_call_node_modules_ACD-2416.py'))
    for node in ast.walk(analyzer.root_ast_node):
        if isinstance(node, ast.Call):
            # os.path.join()
            if isinstance(node.func, ast.Attribute):
                assert analyzer.get_call_node_modules(node) == {'os', 'os.path', 'os.path.join'}
            # other call nodes
            else:
                # assert analyzer.get_call_node_modules(node) == {'os'}
                # now func itself won't be regarded as `os` related
                pass


def test_basic_get_parent_ast_node():

    analyzer = AstAnalyzer(python_file_path=os.path.join(TEST_PACKAGE_ROOT, 'basic_get_parent_ast_node_ACD-2725.py'))
    ast_nodes = analyzer.get_variable_distribution('value')

    assert len(ast_nodes) == 1
    ast_node = ast_nodes[0]
    assert isinstance(ast_node, ast.Name)

    expected_types = [ast.Name, ast.Assign, ast.FunctionDef, ast.ClassDef, ast.Module]
    for expected_type in expected_types:
        assert isinstance(ast_node, expected_type)
        ast_node = analyzer.get_parent_ast_node(ast_node)

    assert ast_node == None


def test_basic_get_code_block():

    analyzer = AstAnalyzer(python_file_path=os.path.join(TEST_PACKAGE_ROOT, 'basic_get_code_block_ACD-2688.py'))

    remove_function = analyzer.get_module_function_call_usage('os', 'remove')[0]
    assert isinstance(analyzer.get_code_block(remove_function), ast.Module)

    write_function = analyzer.get_module_function_call_usage('os', 'write')[0]
    assert isinstance(analyzer.get_code_block(write_function), ast.FunctionDef)

    read_function = analyzer.get_module_function_call_usage('os', 'read')[0]
    assert isinstance(analyzer.get_code_block(read_function), ast.ClassDef)

    kill_function = analyzer.get_module_function_call_usage('os', 'kill')[0]
    assert isinstance(analyzer.get_code_block(kill_function), ast.If)

    open_function = analyzer.get_module_function_call_usage(AstVariable.BUILTIN_TYPE, 'open')[0]
    assert isinstance(analyzer.get_code_block(open_function), ast.With)

    close_function = analyzer.get_module_function_call_usage('os', 'close')[0]
    assert isinstance(analyzer.get_code_block(close_function), ast.For)

    listdir_function = analyzer.get_module_function_call_usage('os', 'listdir')[0]
    code_block = analyzer.get_code_block(listdir_function)
    # here lineno should not be 18
    assert code_block.lineno == 19


def test_basic_is_in_same_code_block():

    analyzer = AstAnalyzer(python_file_path=os.path.join(TEST_PACKAGE_ROOT, 'basic_is_in_same_code_block_ACD-2688.py'))

    read_functions = analyzer.get_module_function_call_usage('os', 'read')
    write_functions = analyzer.get_module_function_call_usage('os', 'write')
    close_functions = analyzer.get_module_function_call_usage('os', 'close')
    kill_functions = analyzer.get_module_function_call_usage('os', 'kill')

    assert len(read_functions) == 2

    for read_function in read_functions:
        for write_function in write_functions:
            for close_function in close_functions:
                if analyzer.is_in_same_code_block([read_function, write_function, close_function]):
                    assert read_function.lineno == 7

    for read_function in read_functions:
        for kill_function in kill_functions:
            if analyzer.is_in_same_code_block([read_function, kill_function]):
                assert read_function.lineno == 5

def test_basic_get_ast_types_in_subtree():

    analyzer = AstAnalyzer(python_file_path=os.path.join(TEST_PACKAGE_ROOT, 'basic_get_ast_types_in_subtree_ACD-2845.py'))
    for node in ast.walk(analyzer.root_ast_node):
        ast_types = set()
        for ast_node in ast.walk(node):
            ast_types.add(type(ast_node))
        assert analyzer.get_ast_types_in_subtree(node) == ast_types


def test_basic_get_ast_nodes_lca():

    if six.PY2:
        analyzer = AstAnalyzer(python_file_path=os.path.join(TEST_PACKAGE_ROOT, 'basic_get_ast_nodes_lca_ACD-2725_py2.py'))
    else:
        analyzer = AstAnalyzer(python_file_path=os.path.join(TEST_PACKAGE_ROOT, 'basic_get_ast_nodes_lca_ACD-2725_py3.py'))

    nodes1 = analyzer.get_variable_distribution('value')
    assert len(nodes1) == 1
    ast_node1 = nodes1[0]

    nodes2 = analyzer.get_variable_distribution('os.path')
    assert len(nodes2) == 1
    ast_node2 = nodes2[0]

    assert analyzer.get_ast_nodes_lca([ast_node1, ast_node2], ast.ClassDef).name == 'A'
    assert analyzer.get_ast_nodes_lca([ast_node1, ast_node2], ast.FunctionDef).name == 'test'
    assert analyzer.get_ast_nodes_lca([ast_node1, ast_node2], ast.Call) == None

    nodes3 = analyzer.get_variable_distribution('a')
    assert len(nodes3) == 1
    ast_node3 = nodes3[0]

    assert isinstance(analyzer.get_ast_nodes_lca([ast_node1, ast_node2, ast_node3], ast.AST), ast.FunctionDef)
    assert analyzer.get_ast_nodes_lca([ast_node1, ast_node2, ast_node3], ast.AST).name == 'test'


def test_basic_exec_usage():

    # ast.Exec only available in python 2
    if six.PY2:
        analyzer = AstAnalyzer(python_file_path=os.path.join(TEST_PACKAGE_ROOT, 'basic_exec_usage_ACD-2725_py2.py'))
        exec_nodes = list(analyzer.exec_usage)
        assert len(exec_nodes) == 1
        assert isinstance(exec_nodes[0], ast.Exec)
        assert exec_nodes[0].lineno == 2


def test_basic_function_call_usage():

    analyzer = AstAnalyzer(python_file_path=os.path.join(TEST_PACKAGE_ROOT, 'basic_function_call_usage_ACD-2725.py'))
    function_nodes = analyzer.function_call_usage
    assert len(function_nodes) == 1
    assert 'func' in function_nodes

    function_node_set = function_nodes['func']
    assert len(function_node_set) == 1

    function_node = function_node_set.pop()
    assert isinstance(function_node, ast.Call)


def test_basic_literal_string_usage():

    analyzer = AstAnalyzer(python_file_path=os.path.join(TEST_PACKAGE_ROOT, 'basic_literal_string_usage_ACD-2725.py'))
    literal_string_usage = analyzer.literal_string_usage

    # 'hello' and 'world'
    assert len(literal_string_usage) == 2
    assert 'hello' in literal_string_usage and 'world' in literal_string_usage

    hello_set = literal_string_usage['hello']
    world_set = literal_string_usage['world']

    assert len(hello_set) == 2
    assert len(world_set) == 2

    assert len(list(filter(lambda node: isinstance(node, ast.Name), hello_set))) == 1
    assert len(list(filter(lambda node: isinstance(node, ast.Str), hello_set))) == 1

    assert len(list(filter(lambda node: isinstance(node, ast.Name), world_set))) == 1
    assert len(list(filter(lambda node: isinstance(node, ast.Str), world_set))) == 1


def test_basic_variable_usage():

    if six.PY2:
        analyzer = AstAnalyzer(python_file_path=os.path.join(TEST_PACKAGE_ROOT, 'basic_variable_usage_ACD-2725_py2.py'))
    else:
        analyzer = AstAnalyzer(python_file_path=os.path.join(TEST_PACKAGE_ROOT, 'basic_variable_usage_ACD-2725_py3.py'))

    variable_usage = analyzer.variable_usage

    assert len(variable_usage) == 3
    assert 'a' in variable_usage and 'b' in variable_usage and 'os' in variable_usage

    assert len(variable_usage['a']) == 4
    assert len(variable_usage['b']) == 2
    assert len(variable_usage['os']) == 1


def test_context_dict_are_isolated():

    if six.PY2:
        analyzer = AstAnalyzer(python_file_path=os.path.join(TEST_PACKAGE_ROOT, 'basic_context_dict_ACD-2725_py2.py'))
    else:
        analyzer = AstAnalyzer(python_file_path=os.path.join(TEST_PACKAGE_ROOT, 'basic_context_dict_ACD-2725_py3.py'))

    context_address_set = set()
    # how many different local context exist
    for _, context in analyzer.context_dict.items():
        context_address_set.add(id(context))
    assert len(analyzer.context_dict) == len(context_address_set)


def test_global_context_dict_are_isolated():

    if six.PY2:
        analyzer = AstAnalyzer(python_file_path=os.path.join(TEST_PACKAGE_ROOT, 'basic_global_context_dict_ACD-2725_py2.py'))
    else:
        analyzer = AstAnalyzer(
            python_file_path=os.path.join(TEST_PACKAGE_ROOT, 'basic_global_context_dict_ACD-2725_py3.py'))

    context_address_set = set()
    # how many different global context exist
    for _, context in analyzer.global_context_dict.items():
        context_address_set.add(id(context))
    assert len(analyzer.global_context_dict) == len(context_address_set)


def test_basic_context_dict():

    if six.PY2:
        analyzer = AstAnalyzer(python_file_path=os.path.join(TEST_PACKAGE_ROOT, 'basic_context_dict_ACD-2725_py2.py'))
        exec_nodes = analyzer.query().propagate_nodes(ast_type = ast.Exec, force_propagate=True).collect()
        exec_nodes.sort(key = lambda node: node.lineno)

        context1 = analyzer.context_dict[exec_nodes[0]]
        context2 = analyzer.context_dict[exec_nodes[1]]

        assert 'os' not in context1.variable_map
        assert 'os' in context2.variable_map and isinstance(context2.variable_map['os'], AstVariable) and \
            'os' in context2.variable_map['os'].variable_type_set


def test_context_dict_key_types():

    if six.PY2:
        analyzer = AstAnalyzer(python_file_path=os.path.join(TEST_PACKAGE_ROOT, 'complicated_python_file_ACD-2725_py2.py'))
    else:
        analyzer = AstAnalyzer(python_file_path=os.path.join(TEST_PACKAGE_ROOT, 'complicated_python_file_ACD-2725_py3.py'))

    context = analyzer.context_dict
    # access protected variable directly
    assert all(map(lambda node: isinstance(node, analyzer._snapshot_ast_types), context.keys()))


def test_basic_global_context_dict():

    if six.PY2:
        analyzer = AstAnalyzer(python_file_path=os.path.join(TEST_PACKAGE_ROOT, 'basic_global_context_dict_ACD-2725_py2.py'))

        exec_nodes = analyzer.query().propagate_nodes(ast_type=ast.Exec, force_propagate=True).collect()
        exec_nodes.sort(key=lambda node: node.lineno)

        global_context1 = analyzer.global_context_dict[exec_nodes[0]]
        global_context2 = analyzer.global_context_dict[exec_nodes[1]]

        assert 'os' not in global_context1
        assert 'os' in global_context2 and isinstance(global_context2['os'], AstVariable) and \
               'os' in global_context2['os'].variable_type_set


def test_global_context_dict_key_types():

    if six.PY2:
        analyzer = AstAnalyzer(python_file_path=os.path.join(TEST_PACKAGE_ROOT, 'complicated_python_file_ACD-2725_py2.py'))
    else:
        analyzer = AstAnalyzer(python_file_path=os.path.join(TEST_PACKAGE_ROOT, 'complicated_python_file_ACD-2725_py3.py'))
    # access protected variable directly
    global_context = analyzer.global_context_dict
    assert all(map(lambda node: isinstance(node, analyzer._snapshot_ast_types), global_context.keys()))


def test_basic_exposed_module_set():

    analyzer = AstAnalyzer(python_file_path=os.path.join(TEST_PACKAGE_ROOT, 'basic_exposed_module_set_ACD-2725.py'))
    exposed_module_set = analyzer.exposed_module_set
    expected_set = {'a', 'func', 'A'}
    assert exposed_module_set == expected_set


def test_exposed_module_set_without_all_attribute():

    analyzer = AstAnalyzer(python_file_path=os.path.join(TEST_PACKAGE_ROOT, 'exposed_module_set_without_all_attribute_ACD-2725.py'))
    exposed_module_set = analyzer.exposed_module_set
    assert exposed_module_set == {'a', 'func', 'A'}


def test_exposed_module_set_with_unparseable_all_attribute():

    analyzer = AstAnalyzer(python_file_path=os.path.join(TEST_PACKAGE_ROOT, 'exposed_module_set_with_unparseable_all_attribute_ACD-2725.py'))
    exposed_module_set = analyzer.exposed_module_set
    assert exposed_module_set == {'value', 'func', '__all__'}


def test_exposed_module_set_with_unparseable_all_attribute_datastructure():

    analyzer = AstAnalyzer(python_file_path=os.path.join(TEST_PACKAGE_ROOT, 'exposed_module_set_with_unparseable_all_attribute_datastructure_ACD-2725.py'))
    exposed_module_set = analyzer.exposed_module_set
    assert exposed_module_set == {'value', 'func', '__all__'}


def test_basic_module():

    analyzer = AstAnalyzer(python_file_path=os.path.join(TEST_PACKAGE_ROOT, 'basic_module_ACD-2725.py'))
    assert isinstance(analyzer.module, AstModule)
    assert len(analyzer.module.global_map) == 3
    assert analyzer.module.name == 'basic_module_ACD-2725'
    assert isinstance(analyzer.module.global_map['a'], AstVariable)
    assert isinstance(analyzer.module.global_map['func'], AstFunction)
    assert isinstance(analyzer.module.global_map['C'], AstClass)

    analyzer = AstAnalyzer(python_code_string='import os')
    assert isinstance(analyzer.module, AstModule)
    assert len(analyzer.module.global_map) == 1
    assert analyzer.module.name == None
    assert isinstance(analyzer.module.global_map['os'], AstVariable)


def test_function_call_alias_usage():

    analyzer = AstAnalyzer(python_file_path=os.path.join(TEST_PACKAGE_ROOT, 'function_call_alias_usage_ACD-2725.py'))
    lineno_list = analyzer.get_module_function_call_usage('shutil', 'rmtree', lineno_only=True)
    assert lineno_list == [4, 7]

    ast_nodes = analyzer.get_module_function_call_usage('shutil', 'rmtree')
    assert len(ast_nodes) == 2
    assert all(filter(lambda node: isinstance(node, ast.Call), ast_nodes)) == True


def test_function_call_chain():

    if six.PY2:
        analyzer = AstAnalyzer(python_file_path=os.path.join(TEST_PACKAGE_ROOT, 'function_call_chain_ACD-2725_py2.py'))
    else:
        analyzer = AstAnalyzer(python_file_path=os.path.join(TEST_PACKAGE_ROOT, 'function_call_chain_ACD-2725_py3.py'))
    lineno_list = analyzer.get_module_usage('os', lineno_only=True)
    assert lineno_list == [1, 12]


def test_import_same_module_multi_times():

    analyzer = AstAnalyzer(python_file_path=os.path.join(TEST_PACKAGE_ROOT, 'import_same_module_multi_times_ACD-2725.py'))
    lineno_list = analyzer.get_module_usage('os', lineno_only=True)
    assert lineno_list == [1, 2, 4]


def test_scan_builtin_function_usage():

    if six.PY2:
        analyzer = AstAnalyzer(python_file_path=os.path.join(TEST_PACKAGE_ROOT, 'scan_builtin_function_usage_ACD-2725_py2.py'))
    else:
        analyzer = AstAnalyzer(python_file_path=os.path.join(TEST_PACKAGE_ROOT, 'scan_builtin_function_usage_ACD-2725_py3.py'))

    lineno_list = analyzer.get_module_usage(AstVariable.BUILTIN_TYPE, lineno_only=True)
    assert lineno_list == [1, 2, 4]

    ast_node = analyzer.get_variable_distribution('f')[0]
    variable = analyzer.get_variable_details(ast_node)
    assert 'file' in variable.variable_type_set


def test_specific_builtin_function_usage():

    if six.PY2:
        analyzer = AstAnalyzer(python_file_path=os.path.join(TEST_PACKAGE_ROOT, 'specific_builtin_function_usage_ACD-2725_py2.py'))
    else:
        analyzer = AstAnalyzer(python_file_path=os.path.join(TEST_PACKAGE_ROOT, 'specific_builtin_function_usage_ACD-2725_py3.py'))
    lineno_list = analyzer.get_module_usage(AstVariable.BUILTIN_TYPE + '.' + '__import__', lineno_only=True)
    assert lineno_list == [5]


def test_specific_builtin_function_call_usage():

    if six.PY2:
        analyzer = AstAnalyzer(python_file_path=os.path.join(TEST_PACKAGE_ROOT, 'specific_builtin_function_call_usage_ACD-2725_py2.py'))
    else:
        analyzer = AstAnalyzer(python_file_path=os.path.join(TEST_PACKAGE_ROOT, 'specific_builtin_function_call_usage_ACD-2725_py3.py'))
    # function name could be None
    lineno_list = analyzer.get_module_function_call_usage(AstVariable.BUILTIN_TYPE, lineno_only=True, fuzzy=True)
    assert lineno_list == [4]
    # specify __import__ function
    lineno_list = analyzer.get_module_function_call_usage(AstVariable.BUILTIN_TYPE, '__import__', lineno_only=True)
    assert lineno_list == [4]
    # compared with module usage result
    lineno_list = analyzer.get_module_usage(AstVariable.BUILTIN_TYPE + '.' + '__import__', lineno_only=True)
    assert lineno_list == [3, 4]


def test_local_variable_access():

    if six.PY2:
        analyzer = AstAnalyzer(python_file_path=os.path.join(TEST_PACKAGE_ROOT, 'local_variable_access_ACD-2725_py2.py'))
    else:
        analyzer = AstAnalyzer(python_file_path=os.path.join(TEST_PACKAGE_ROOT, 'local_variable_access_ACD-2725_py3.py'))
    lineno_list = analyzer.get_module_usage('os', lineno_only=True)
    assert lineno_list == [1, 5]


def test_instance_attribute_access():

    if six.PY2:
        analyzer = AstAnalyzer(python_file_path=os.path.join(TEST_PACKAGE_ROOT, 'instance_attribute_access_ACD-2725_py2.py'))
    else:
        analyzer = AstAnalyzer(python_file_path=os.path.join(TEST_PACKAGE_ROOT, 'instance_attribute_access_ACD-2725_py3.py'))
    lineno_list = analyzer.get_module_usage('os', lineno_only=True)
    assert lineno_list == [1, 4, 7]


def test_class_attribute_access():

    if six.PY2:
        analyzer = AstAnalyzer(python_file_path=os.path.join(TEST_PACKAGE_ROOT, 'class_attribute_access_ACD-2725_py2.py'))
    else:
        analyzer = AstAnalyzer(python_file_path=os.path.join(TEST_PACKAGE_ROOT, 'class_attribute_access_ACD-2725_py3.py'))
    lineno_list = analyzer.get_module_usage('os', lineno_only=True)
    assert lineno_list == [1, 4, 6]


def test_use_function_call_return_value():

    if six.PY2:
        analyzer = AstAnalyzer(python_file_path=os.path.join(TEST_PACKAGE_ROOT, 'use_function_call_return_value_ACD-2725_py2.py'))
    else:
        analyzer = AstAnalyzer(python_file_path=os.path.join(TEST_PACKAGE_ROOT, 'use_function_call_return_value_ACD-2725_py3.py'))
    lineno_list = analyzer.get_module_usage('os', lineno_only=True)
    assert lineno_list == [2, 5, 7]


def test_builtin_import_usage():

    if six.PY2:
        analyzer = AstAnalyzer(python_file_path=os.path.join(TEST_PACKAGE_ROOT, 'builtin_import_usage_ACD-2725_py2.py'))
    else:
        analyzer = AstAnalyzer(python_file_path=os.path.join(TEST_PACKAGE_ROOT, 'builtin_import_usage_ACD-2725_py3.py'))
    lineno_list = analyzer.get_module_usage('os', lineno_only=True)
    assert lineno_list == [1, 3]

    lineno_list = analyzer.get_module_function_call_usage('os', lineno_only=True, fuzzy=True)
    assert lineno_list == [3]


def test_function_default_arguments():

    if six.PY2:
        analyzer = AstAnalyzer(python_file_path=os.path.join(TEST_PACKAGE_ROOT, 'function_default_arguments_ACD-2725_py2.py'))
    else:
        analyzer = AstAnalyzer(python_file_path=os.path.join(TEST_PACKAGE_ROOT, 'function_default_arguments_ACD-2725_py3.py'))
    lineno_list = analyzer.get_module_usage('os', lineno_only=True)
    assert lineno_list == [1, 3, 4]


def test_inherited_class_attribute_usage():

    if six.PY2:
        analyzer = AstAnalyzer(python_file_path=os.path.join(TEST_PACKAGE_ROOT, 'inherited_class_attribute_usage_ACD-2725_py2.py'))
    else:
        analyzer = AstAnalyzer(python_file_path=os.path.join(TEST_PACKAGE_ROOT, 'inherited_class_attribute_usage_ACD-2725_py3.py'))
    lineno_list = analyzer.get_module_usage('os', lineno_only=True)
    assert lineno_list == [1, 4, 10]


def test_module_usage_with_control_flow():

    if six.PY2:
        analyzer = AstAnalyzer(python_file_path=os.path.join(TEST_PACKAGE_ROOT, 'module_usage_with_control_flow_ACD-2725_py2.py'))
    else:
        analyzer = AstAnalyzer(python_file_path=os.path.join(TEST_PACKAGE_ROOT, 'module_usage_with_control_flow_ACD-2725_py3.py'))
    lineno_list = analyzer.get_module_usage('os', lineno_only=True)
    assert lineno_list == [2, 8]

    lineno_list = analyzer.get_module_usage('sys', lineno_only=True)
    assert lineno_list == [5, 8]


def test_exception_variable_with_module_name_usage():

    if six.PY2:
        analyzer = AstAnalyzer(python_file_path=os.path.join(TEST_PACKAGE_ROOT, 'exception_variable_with_module_name_usage_ACD-2725_py2.py'))
    else:
        analyzer = AstAnalyzer(python_file_path=os.path.join(TEST_PACKAGE_ROOT, 'exception_variable_with_module_name_usage_ACD-2725_py3.py'))
    lineno_list = analyzer.get_module_usage('os', lineno_only=True)
    assert lineno_list == [1]


def test_simple_lambda_usage():

    if six.PY2:
        analyzer = AstAnalyzer(python_file_path=os.path.join(TEST_PACKAGE_ROOT, 'simple_lambda_usage_ACD-2725_py2.py'))
    else:
        analyzer = AstAnalyzer(python_file_path=os.path.join(TEST_PACKAGE_ROOT, 'simple_lambda_usage_ACD-2725_py3.py'))
    lineno_list = analyzer.get_module_usage('os', lineno_only=True)
    assert lineno_list == [1, 3, 4]


def test_set_attribute_usage():

    if six.PY2:
        analyzer = AstAnalyzer(python_file_path=os.path.join(TEST_PACKAGE_ROOT, 'set_attribute_usage_ACD-2725_py2.py'))
    else:
        analyzer = AstAnalyzer(python_file_path=os.path.join(TEST_PACKAGE_ROOT, 'set_attribute_usage_ACD-2725_py3.py'))
    lineno_list = analyzer.get_module_usage('os', lineno_only=True)
    assert lineno_list == [1, 7, 8]


def test_get_attribute_usage():

    if six.PY2:
        analyzer = AstAnalyzer(python_file_path=os.path.join(TEST_PACKAGE_ROOT, 'get_attribute_usage_ACD-2725_py2.py'))
    else:
        analyzer = AstAnalyzer(python_file_path=os.path.join(TEST_PACKAGE_ROOT, 'get_attribute_usage_ACD-2725_py3.py'))
    lineno_list = analyzer.get_module_usage('os', lineno_only=True)
    assert lineno_list == [1, 4, 7, 9]


def test_import_system_libraries():

    class ModuleManager:
        def load_modules(self, module_string):
            if module_string == 'test':
                ast_module = AstModule('test')
                return [ast_module]
            else:
                return []

    if six.PY2:
        analyzer = AstAnalyzer(python_file_path=os.path.join(TEST_PACKAGE_ROOT, 'import_system_libraries_ACD-2725_py2.py'),
                           module_manager=ModuleManager())
    else:
        analyzer = AstAnalyzer(python_file_path=os.path.join(TEST_PACKAGE_ROOT, 'import_system_libraries_ACD-2725_py3.py'),
                               module_manager=ModuleManager())

    lineno_list = analyzer.get_module_usage('test', lineno_only=True)
    assert lineno_list == [2]

    lineno_list = analyzer.get_module_usage('os', lineno_only=True)
    assert lineno_list == [1, 4]


def test_load_module_from_outside():

    class ModuleManager:
        def load_modules(self, module_string):
            assert module_string == 'test'
            # mock load module here
            module = AstModule('test')
            module.global_map['func'] = AstFunction('func', None, AstVariable(None, {'os'}))
            return [module]

    if six.PY2:
        analyzer = AstAnalyzer(python_file_path=os.path.join(TEST_PACKAGE_ROOT, 'load_module_from_outside_ACD-2725_py2.py'),
                           module_manager=ModuleManager())
    else:
        analyzer = AstAnalyzer(python_file_path=os.path.join(TEST_PACKAGE_ROOT, 'load_module_from_outside_ACD-2725_py3.py'),
                               module_manager=ModuleManager())
    lineno_list = analyzer.get_module_usage('os', lineno_only=True)
    assert lineno_list == [3]


def test_load_external_module_in_nested_context():

    class ModuleManager:
        def load_modules(self, module_string):
            assert module_string == 'test.f'
            ast_function = AstFunction('f', None, return_value=AstVariable(None, {'os'}))
            return [ast_function]

    if six.PY2:
        analyzer = AstAnalyzer(python_file_path=os.path.join(TEST_PACKAGE_ROOT, 'load_external_module_in_nested_context_ACD-2725_py2.py'),
                           module_manager=ModuleManager())
    else:
        analyzer = AstAnalyzer(python_file_path=os.path.join(TEST_PACKAGE_ROOT, 'load_external_module_in_nested_context_ACD-2725_py3.py'),
            module_manager=ModuleManager())
    lineno_list = analyzer.get_module_usage('os', lineno_only=True)
    assert lineno_list == [3]


def test_load_module_with_alias_from_outside():

    class ModuleManager:
        def load_modules(self, module_string):
            assert module_string == 'test'
            # mock load module here
            module = AstModule('test')
            module.global_map['func'] = AstFunction('func', None, AstVariable(None, {'os'}))
            return [module]

    if six.PY2:
        analyzer = AstAnalyzer(python_file_path=os.path.join(TEST_PACKAGE_ROOT, 'load_module_with_alias_from_outside_ACD-2725_py2.py'),
                           module_manager=ModuleManager())
    else:
        analyzer = AstAnalyzer(python_file_path=os.path.join(TEST_PACKAGE_ROOT, 'load_module_with_alias_from_outside_ACD-2725_py3.py'),
            module_manager=ModuleManager())
    lineno_list = analyzer.get_module_usage('os', lineno_only=True)
    assert lineno_list == [3]

    assert isinstance(analyzer.module.global_map['t'], AstModule)
    assert analyzer.module.global_map['t'].name == 't'


def test_load_external_submodule_with_alias():

    class ModuleManager:
        def load_modules(self, module_string):
            assert module_string == 'a.b'
            return []

    AstAnalyzer(python_file_path=os.path.join(TEST_PACKAGE_ROOT, 'load_external_submodule_with_alias_ACD-2861.py'),
                           module_manager=ModuleManager())


def test_load_function_from_outside():

    class ModuleManager:
        def load_modules(self, module_string):
            # mock load function here
            assert module_string == 'test.func'
            func = AstFunction('func', None, AstVariable(None, {'os'}))
            return [func]

    if six.PY2:
        analyzer = AstAnalyzer(python_file_path=os.path.join(TEST_PACKAGE_ROOT, 'load_function_from_outside_ACD-2725_py2.py'),
                           module_manager=ModuleManager())
    else:
        analyzer = AstAnalyzer(python_file_path=os.path.join(TEST_PACKAGE_ROOT, 'load_function_from_outside_ACD-2725_py3.py'),
            module_manager=ModuleManager())
    lineno_list = analyzer.get_module_usage('os', lineno_only=True)
    assert lineno_list == [2]


def test_load_class_from_outside():

    class ModuleManager:
        def load_modules(self, module_string):
            assert module_string == 'test.A'
            ast_context = AstContext(0, None)
            ast_context.variable_map['value'] = AstVariable(None, {'os'}, name = 'value')
            ast_class = AstClass('A', ast_context)
            return [ast_class]

    if six.PY2:
        analyzer = AstAnalyzer(python_file_path=os.path.join(TEST_PACKAGE_ROOT, 'load_class_from_outside_ACD-2725_py2.py'),
                           module_manager=ModuleManager())
    else:
        analyzer = AstAnalyzer(python_file_path=os.path.join(TEST_PACKAGE_ROOT, 'load_class_from_outside_ACD-2725_py3.py'),
                               module_manager=ModuleManager())
    lineno_list = analyzer.get_module_usage('os', lineno_only=True)
    assert lineno_list == [4]


def test_load_attribute_from_outside():

    class ModuleManager:
        def load_modules(self, module_string):
            assert module_string == 'test.attr'
            ast_variable = AstVariable(None, {'os'}, name = 'attr')
            return [ast_variable]

    if six.PY2:
        analyzer = AstAnalyzer(python_file_path=os.path.join(TEST_PACKAGE_ROOT, 'load_attribute_from_outside_ACD-2725_py2.py'),
                           module_manager=ModuleManager())
    else:
        analyzer = AstAnalyzer(python_file_path=os.path.join(TEST_PACKAGE_ROOT, 'load_attribute_from_outside_ACD-2725_py3.py'),
            module_manager=ModuleManager())
    lineno_list = analyzer.get_module_usage('os', lineno_only=True)
    assert lineno_list == [3]


def test_load_external_module_with_builtin_import():

    class ModuleManager:
        def load_modules(self, module_string):
            assert module_string == 'test'
            ast_module = AstModule('test')
            ast_module.global_map['func'] = AstFunction('func', None, AstVariable(None, {'os'}))
            return [ast_module]

    if six.PY2:
        analyzer = AstAnalyzer(python_file_path=os.path.join(TEST_PACKAGE_ROOT, 'load_external_module_with_builtin_import_ACD-2725_py2.py'),
                           module_manager=ModuleManager())
    else:
        analyzer = AstAnalyzer(python_file_path=os.path.join(TEST_PACKAGE_ROOT, 'load_external_module_with_builtin_import_ACD-2725_py3.py'),
                           module_manager=ModuleManager())
    lineno_list = analyzer.get_module_usage('os', lineno_only=True)
    assert lineno_list == [2]


def test_load_external_nested_module_with_builtin_import():

    class ModuleManager:
        def load_modules(self, module_string):
            assert module_string == 'test'
            ast_module = AstModule('test')
            ast_module.global_map['module'] = AstModule('module')
            ast_module.global_map['module'].global_map['func'] = AstFunction('func', None, AstVariable(None, {'os'}))
            return [ast_module]

    if six.PY2:
        analyzer = AstAnalyzer(python_file_path=os.path.join(TEST_PACKAGE_ROOT, 'load_external_nested_module_with_builtin_import_ACD-2725_py2.py'),
                           module_manager=ModuleManager())
    else:
        analyzer = AstAnalyzer(python_file_path=os.path.join(TEST_PACKAGE_ROOT, 'load_external_nested_module_with_builtin_import_ACD-2725_py3.py'),
                               module_manager=ModuleManager())
    lineno_list = analyzer.get_module_usage('os', lineno_only=True)
    assert lineno_list == [3]


def test_sensitive_string_usage():

    if six.PY2:
        analyzer = AstAnalyzer(python_file_path=os.path.join(TEST_PACKAGE_ROOT, 'sensitive_string_usage_ACD-2725_py2.py'))
    else:
        analyzer = AstAnalyzer(python_file_path=os.path.join(TEST_PACKAGE_ROOT, 'sensitive_string_usage_ACD-2725_py3.py'))
    lineno_list = analyzer.get_module_usage('os', lineno_only=True)
    assert lineno_list == [1, 4, 6]


def test_advanced_get_module_usage():

    if six.PY2:
        analyzer = AstAnalyzer(python_file_path=os.path.join(TEST_PACKAGE_ROOT, 'advanced_get_module_usage_ACD-2725_py2.py'))
    else:
        analyzer = AstAnalyzer(python_file_path=os.path.join(TEST_PACKAGE_ROOT, 'advanced_get_module_usage_ACD-2725_py3.py'))
    lineno_list = analyzer.get_module_usage('os.path', lineno_only=True)
    assert lineno_list == [3]

    nodes = analyzer.get_module_usage('os.path')
    assert len(nodes) == 3
    assert len(list(filter(lambda node: isinstance(node, ast.Attribute), nodes))) == 2
    assert len(list(filter(lambda node: isinstance(node, ast.Call), nodes))) == 1


def test_advanced_get_module_function_call_usage():

    analyzer = AstAnalyzer(python_file_path=os.path.join(TEST_PACKAGE_ROOT, 'advanced_get_module_function_call_usage_ACD-2725.py'))
    lineno_list = analyzer.get_module_function_call_usage('socket.socket', lineno_only=True)
    assert lineno_list == [3]

    nodes = analyzer.get_module_function_call_usage('socket.socket')
    assert len(nodes) == 1
    assert isinstance(nodes[0], ast.Call)


def test_advanced_get_module_usage_with_complicated_class_combination():

    if six.PY2:
        analyzer = AstAnalyzer(python_file_path=os.path.join(TEST_PACKAGE_ROOT, 'advanced_get_module_usage_with_complicated_class_combination_ACD-2725_py2.py'))
    else:
        analyzer = AstAnalyzer(python_file_path=os.path.join(TEST_PACKAGE_ROOT, 'advanced_get_module_usage_with_complicated_class_combination_ACD-2725_py3.py'))
    lineno_list = analyzer.get_module_usage('os', lineno_only=True)
    assert lineno_list == [1, 16]


def test_get_literal_string_usage():

    analyzer = AstAnalyzer(python_file_path=os.path.join(TEST_PACKAGE_ROOT, 'advanced_get_literal_string_usage_ACD-2725.py'))
    lineno_list = analyzer.get_literal_string_usage('hello world', lineno_only=True)
    assert lineno_list == [6]

    lineno_list = analyzer.get_literal_string_usage('h.*d', lineno_only=True)
    assert lineno_list == [6]


def test_import_external_module():

    class ModuleManager:
        def load_modules(self, module_string):
            assert module_string == 'os'
            return []

    AstAnalyzer(python_file_path=os.path.join(TEST_PACKAGE_ROOT, 'import_external_module_ACD-2725.py'), module_manager=ModuleManager())


def test_from_import_external_module():

    class ModuleManager:
        def load_modules(self, module_string):
            assert module_string == 'a.b'
            return []

    AstAnalyzer(python_file_path=os.path.join(TEST_PACKAGE_ROOT, 'from_import_external_module_ACD-2725.py'), module_manager=ModuleManager())


def test_complicated_from_import_external_module():

    class ModuleManager:
        def load_modules(self, module_string):
            assert module_string == '....sfd.b'
            return []

    AstAnalyzer(python_file_path=os.path.join(TEST_PACKAGE_ROOT, 'complicated_from_import_external_module_ACD-2725.py'), module_manager=ModuleManager())


def test_from_import_external_module_with_consecutive_dot():

    class ModuleManager:
        def load_modules(self, module_string):
            assert module_string == '.....test'
            return []

    AstAnalyzer(python_file_path=os.path.join(TEST_PACKAGE_ROOT, 'from_import_external_module_with_consecutive_dot_ACD-2725.py'),
                           module_manager=ModuleManager())


def test_module_used_in_some_uncommon_expression():

    if six.PY2:
        analyzer = AstAnalyzer(python_file_path=os.path.join(TEST_PACKAGE_ROOT, 'module_used_in_some_uncommon_expression_ACD-2725_py2.py'))
    else:
        analyzer = AstAnalyzer(python_file_path=os.path.join(TEST_PACKAGE_ROOT, 'module_used_in_some_uncommon_expression_ACD-2725_py3.py'))
    lineno_list = analyzer.get_module_usage('os', lineno_only=True)
    assert lineno_list == [1, 3]


def test_complicated_builtin_import_usage():

    if six.PY2:
        analyzer = AstAnalyzer(python_file_path=os.path.join(TEST_PACKAGE_ROOT, 'complicated_builtin_import_usage_ACD-2725_py2.py'))
    else:
        analyzer = AstAnalyzer(python_file_path=os.path.join(TEST_PACKAGE_ROOT, 'complicated_builtin_import_usage_ACD-2725_py3.py'))
    lineno_list = analyzer.get_module_usage('os', lineno_only=True)
    assert lineno_list == [4, 5]


    lineno_list = analyzer.get_module_function_call_usage('os', lineno_only=True, fuzzy=True)
    assert lineno_list == [5]


def test_load_external_nested_module_with_builtin_import_and_without_module_manager():

    if six.PY2:
        analyzer = AstAnalyzer(python_file_path=os.path.join(TEST_PACKAGE_ROOT, 'load_external_nested_module_with_builtin_import_and_without_module_manager_ACD-2725_py2.py'))
    else:
        analyzer = AstAnalyzer(python_file_path=os.path.join(TEST_PACKAGE_ROOT, 'load_external_nested_module_with_builtin_import_and_without_module_manager_ACD-2725_py3.py'))
    lineno_list = analyzer.get_module_usage('a', lineno_only=True)
    assert lineno_list == [1, 2]

    lineno_list = analyzer.get_module_usage('a.b', lineno_only=True)
    assert lineno_list == [1, 2]


def test_load_external_module_with_builtin_import_and_module_manager_return_empty_list():

    class ModuleManager:
        def load_modules(self, module_string):
            assert module_string == 'os'
            return []

    if six.PY2:
        analyzer = AstAnalyzer(python_file_path=os.path.join(TEST_PACKAGE_ROOT, 'load_external_module_with_builtin_import_and_module_manager_return_empty_list_ACD-2725_py2.py'),
                           module_manager=ModuleManager())
    else:
        analyzer = AstAnalyzer(python_file_path=os.path.join(TEST_PACKAGE_ROOT, 'load_external_module_with_builtin_import_and_module_manager_return_empty_list_ACD-2725_py3.py'),
                               module_manager=ModuleManager())
    lineno_list = analyzer.get_module_usage('os', lineno_only=True)
    assert lineno_list == [1, 2]


def test_load_external_module_with_alias_and_module_manager_return_empty_list():

    class ModuleManager:
        def load_modules(self, module_string):
            assert module_string == 'a.b'
            return []

    if six.PY2:
        analyzer = AstAnalyzer(python_file_path=os.path.join(TEST_PACKAGE_ROOT, 'load_external_module_with_alias_and_module_manager_return_empty_list_ACD-2725_py2.py'),
                           module_manager=ModuleManager())
    else:
        analyzer = AstAnalyzer(python_file_path=os.path.join(TEST_PACKAGE_ROOT, 'load_external_module_with_alias_and_module_manager_return_empty_list_ACD-2725_py3.py'),
                               module_manager=ModuleManager())
    lineno_list = analyzer.get_module_usage('a', lineno_only=True)
    assert lineno_list == [1, 3]

    lineno_list = analyzer.get_module_usage('a.b', lineno_only=True)
    assert lineno_list == [1, 3]


def test_load_external_module_with_builtin_import_and_unparseable_augument():

    class ModuleManager:
        def load_modules(self, module_string):
            # it won't be triggered
            assert False

    if six.PY2:
        analyzer = AstAnalyzer(python_file_path=os.path.join(TEST_PACKAGE_ROOT, 'load_external_module_with_builtin_import_and_unparseable_augument_ACD-2725_py2.py'),
                           module_manager=ModuleManager())
    else:
        analyzer = AstAnalyzer(python_file_path=os.path.join(TEST_PACKAGE_ROOT, 'load_external_module_with_builtin_import_and_unparseable_augument_ACD-2725_py3.py'),
                               module_manager=ModuleManager())
    lineno_list = analyzer.get_module_usage('os', lineno_only=True)
    assert lineno_list == []


def test_class_attribute_self_access():

    if six.PY2:
        analyzer = AstAnalyzer(python_file_path=os.path.join(TEST_PACKAGE_ROOT, 'class_attribute_self_access_ACD-2725_py2.py'))
    else:
        analyzer = AstAnalyzer(python_file_path=os.path.join(TEST_PACKAGE_ROOT, 'class_attribute_self_access_ACD-2725_py3.py'))
    lineno_list = analyzer.get_module_usage('os', lineno_only=True)
    assert lineno_list == [1, 4, 7]


def test_manipulate_class_attribute():

    if six.PY2:
        analyzer = AstAnalyzer(python_file_path=os.path.join(TEST_PACKAGE_ROOT, 'manipulate_class_attribute_ACD-2725_py2.py'))
    else:
        analyzer = AstAnalyzer(python_file_path=os.path.join(TEST_PACKAGE_ROOT, 'manipulate_class_attribute_ACD-2725_py3.py'))
    lineno_list = analyzer.get_module_usage('os', lineno_only=True)
    assert lineno_list == [1, 7, 8]


def test_simple_datastructure_combination():

    if six.PY2:
        analyzer = AstAnalyzer(python_file_path=os.path.join(TEST_PACKAGE_ROOT, 'simple_datastructure_combination_ACD-2725_py2.py'))
    else:
        analyzer = AstAnalyzer(python_file_path=os.path.join(TEST_PACKAGE_ROOT, 'simple_datastructure_combination_ACD-2725_py3.py'))
    lineno_list = analyzer.get_module_usage('os', lineno_only=True)
    assert lineno_list == [1, 3, 4]


def test_variable_used_then_deleted():

    if six.PY2:
        analyzer = AstAnalyzer(python_file_path=os.path.join(TEST_PACKAGE_ROOT, 'variable_used_then_deleted_ACD-2725_py2.py'))
    else:
        analyzer = AstAnalyzer(python_file_path=os.path.join(TEST_PACKAGE_ROOT, 'variable_used_then_deleted_ACD-2725_py3.py'))
    lineno_list = analyzer.get_module_usage('os', lineno_only=True)
    assert lineno_list == [1, 3, 4]


def test_delete_class_attribute():

    if six.PY2:
        analyzer = AstAnalyzer(python_file_path=os.path.join(TEST_PACKAGE_ROOT, 'delete_class_attribute_ACD-2725_py2.py'))
    else:
        analyzer = AstAnalyzer(python_file_path=os.path.join(TEST_PACKAGE_ROOT, 'delete_class_attribute_ACD-2725_py3.py'))
    lineno_list = analyzer.get_module_usage('os', lineno_only=True)
    assert lineno_list == [1, 7]


def test_delete_nested_class_attribute():

    if six.PY2:
        analyzer = AstAnalyzer(python_file_path=os.path.join(TEST_PACKAGE_ROOT, 'delete_nested_class_attribute_ACD-2725_py2.py'))
    else:
        analyzer = AstAnalyzer(python_file_path=os.path.join(TEST_PACKAGE_ROOT, 'delete_nested_class_attribute_ACD-2725_py3.py'))
    lineno_list = analyzer.get_module_usage('os', lineno_only=True)
    assert lineno_list == [1, 10]


def test_class_and_function_combination():

    if six.PY2:
        analyzer = AstAnalyzer(python_file_path=os.path.join(TEST_PACKAGE_ROOT, 'class_and_function_combination_ACD-2725_py2.py'))
    else:
        analyzer = AstAnalyzer(python_file_path=os.path.join(TEST_PACKAGE_ROOT, 'class_and_function_combination_ACD-2725_py3.py'))
    lineno_list = analyzer.get_module_usage('os', lineno_only=True)
    assert lineno_list == [1, 7, 10]


def test_simple_closure_functionality():

    if six.PY2:
        analyzer = AstAnalyzer(python_file_path=os.path.join(TEST_PACKAGE_ROOT, 'simple_closure_functionality_ACD-2725_py2.py'))
    else:
        analyzer = AstAnalyzer(python_file_path=os.path.join(TEST_PACKAGE_ROOT, 'simple_closure_functionality_ACD-2725_py3.py'))
    lineno_list = analyzer.get_module_usage('os', lineno_only=True)
    assert lineno_list == [1, 8]


def test_inherited_class_method_usage():

    if six.PY2:
        analyzer = AstAnalyzer(python_file_path=os.path.join(TEST_PACKAGE_ROOT, 'inherited_class_method_usage_ACD-2725_py2.py'))
    else:
        analyzer = AstAnalyzer(python_file_path=os.path.join(TEST_PACKAGE_ROOT, 'inherited_class_method_usage_ACD-2725_py3.py'))
    lineno_list = analyzer.get_module_usage('os', lineno_only=True)
    assert lineno_list == [1, 13]


def test_class_initialization_order():

    if six.PY2:
        analyzer = AstAnalyzer(python_file_path=os.path.join(TEST_PACKAGE_ROOT, 'class_initialization_order_ACD-2725_py2.py'))
    else:
        analyzer = AstAnalyzer(python_file_path=os.path.join(TEST_PACKAGE_ROOT, 'class_initialization_order_ACD-2725_py3.py'))
    lineno_list = analyzer.get_module_usage('os', lineno_only=True)
    assert lineno_list == [1, 5]


def test_module_prefix_check():

    analyzer = AstAnalyzer(python_file_path=os.path.join(TEST_PACKAGE_ROOT, 'module_prefix_check_ACD-2725.py'))
    lineno_list = analyzer.get_module_all_possible_usage('o', lineno_only=True)
    assert lineno_list == []

    lineno_list = analyzer.get_module_all_possible_usage('os', lineno_only=True)
    assert lineno_list == [1]

    lineno_list = analyzer.get_module_all_possible_usage('a.b', lineno_only=True)
    assert lineno_list == [3]

    lineno_list = analyzer.get_module_all_possible_usage('ab', lineno_only=True)
    assert lineno_list == []

    lineno_list = analyzer.get_module_all_possible_usage('', lineno_only=True)
    assert lineno_list == []

    lineno_list = analyzer.get_module_all_possible_usage('.', lineno_only=True)
    assert lineno_list == []


def test_module_usage_in_for_loop():

    if six.PY2:
        analyzer = AstAnalyzer(os.path.join(TEST_PACKAGE_ROOT, 'module_usage_in_for_loop_ACD-2725_py2.py'))
    else:
        analyzer = AstAnalyzer(os.path.join(TEST_PACKAGE_ROOT, 'module_usage_in_for_loop_ACD-2725_py3.py'))
    lineno_list = analyzer.get_module_usage('os', lineno_only=True)
    assert lineno_list == [1, 3, 5, 7]

    ast_node = analyzer.get_variable_distribution('module')[0]
    variable = analyzer.get_variable_details(ast_node)

    assert {'os'} == variable.variable_type_set


def test_local_variable_cover_global_variable():

    if six.PY2:
        analyzer = AstAnalyzer(os.path.join(TEST_PACKAGE_ROOT, 'local_variable_cover_global_variable_ACD-2725_py2.py'))
    else:
        analyzer = AstAnalyzer(os.path.join(TEST_PACKAGE_ROOT, 'local_variable_cover_global_variable_ACD-2725_py3.py'))
    lineno_list = analyzer.get_module_usage('os', lineno_only=True)
    assert lineno_list == [1, 7]


def test_manipulate_global_variable_directly():

    if six.PY2:
        analyzer = AstAnalyzer(os.path.join(TEST_PACKAGE_ROOT, 'manipulate_global_variable_directly_ACD-2725_py2.py'))
    else:
        analyzer = AstAnalyzer(os.path.join(TEST_PACKAGE_ROOT, 'manipulate_global_variable_directly_ACD-2725_py3.py'))
    lineno_list = analyzer.get_module_usage('os', lineno_only=True)
    # According to current design, line 12 won't be reported
    assert lineno_list == [1, 8]


def test_read_global_variable_in_nested_context():

    if six.PY2:
        analyzer = AstAnalyzer(os.path.join(TEST_PACKAGE_ROOT, 'read_global_variable_in_nested_context_ACD-2725_py2.py'))
    else:
        analyzer = AstAnalyzer(os.path.join(TEST_PACKAGE_ROOT, 'read_global_variable_in_nested_context_ACD-2725_py3.py'))
    lineno_list = analyzer.get_module_usage('os', lineno_only=True)
    assert lineno_list == [1, 9, 11, 13]


def test_tuple_variables_assignation():

    if six.PY2:
        analyzer = AstAnalyzer(os.path.join(TEST_PACKAGE_ROOT, 'tuple_variables_assignation_ACD-2725_py2.py'))
    else:
        analyzer = AstAnalyzer(os.path.join(TEST_PACKAGE_ROOT, 'tuple_variables_assignation_ACD-2725_py3.py'))
    lineno_list = analyzer.get_module_usage('os', lineno_only=True)
    assert lineno_list == [1, 6]

    lineno_list = analyzer.get_module_usage('sys', lineno_only=True)
    assert lineno_list == [2, 7]


def test_object_in_object():

    if six.PY2:
        analyzer = AstAnalyzer(os.path.join(TEST_PACKAGE_ROOT, 'object_in_object_ACD-2725_py2.py'))
    else:
        analyzer = AstAnalyzer(os.path.join(TEST_PACKAGE_ROOT, 'object_in_object_ACD-2725_py3.py'))
    lineno_list = analyzer.get_module_usage('os', lineno_only=True)
    assert lineno_list == [1, 13]


def test_variable_types_collected_in_collect_mode():

    if six.PY2:
        analyzer = AstAnalyzer(os.path.join(TEST_PACKAGE_ROOT, 'variable_types_collected_in_collect_mode_ACD-2725_py2.py'))
    else:
        analyzer = AstAnalyzer(os.path.join(TEST_PACKAGE_ROOT, 'variable_types_collected_in_collect_mode_ACD-2725_py3.py'))
    lineno_list = analyzer.get_module_usage('os', lineno_only=True)
    assert lineno_list == [1, 7]

    # we want to check last node
    node = list(filter(lambda node: node.lineno == 7, analyzer.get_variable_distribution('value')))[0]
    variable = analyzer.get_variable_details(node)
    assert {'os', 'num'} == variable.variable_type_set


def test_delete_builtin_functions():

    if six.PY2:
        analyzer = AstAnalyzer(os.path.join(TEST_PACKAGE_ROOT, 'delete_builtin_functions_ACD-2725_py2.py'))
    else:
        analyzer = AstAnalyzer(os.path.join(TEST_PACKAGE_ROOT, 'delete_builtin_functions_ACD-2725_py3.py'))
    lineno_list = analyzer.get_module_usage('builtin', lineno_only=True)
    assert lineno_list == []


def test_module_inheritance_usage():

    if six.PY2:
        analyzer = AstAnalyzer(os.path.join(TEST_PACKAGE_ROOT, 'module_inheritance_usage_ACD-2725_py2.py'))
    else:
        analyzer = AstAnalyzer(os.path.join(TEST_PACKAGE_ROOT, 'module_inheritance_usage_ACD-2725_py3.py'))
    lineno_list = analyzer.get_module_function_call_usage('socket', 'connect', lineno_only=True)
    assert lineno_list == [7]

    lineno_list = analyzer.get_module_function_call_usage('socket.socket', 'connect', lineno_only=True)
    assert lineno_list == [7]


def test_get_module_function_call_usage_only_return_call_nodes():

    for root, dirs, files in os.walk(TEST_PACKAGE_ROOT):
        for f in files:
            file_path = os.path.join(root, f)

            two_compatible, three_compatible = True, True
            if "py2" in file_path:
                two_compatible, three_compatible = True, False
            elif "py3" in file_path:
                two_compatible, three_compatible = False, True

            if (six.PY2 and two_compatible) or ((not six.PY2) and three_compatible):
                analyzer = AstAnalyzer(file_path)
            else:
                continue

            # try some common function call usage search
            modules = ['os', 'sys', 're', 'shutil', 'csv']
            for module in modules:
                nodes = analyzer.get_module_function_call_usage(module)
                assert all(map(lambda node: isinstance(node, ast.Call), nodes))


def test_get_module_usage_only_return_limited_nodes():

    for root, dirs, files in os.walk(TEST_PACKAGE_ROOT):
        for f in files:
            file_path = os.path.join(root, f)

            two_compatible, three_compatible = True, True
            if "py2" in file_path:
                two_compatible, three_compatible = True, False
            elif "py3" in file_path:
                two_compatible, three_compatible = False, True

            if (six.PY2 and two_compatible) or ((not six.PY2) and three_compatible):
                analyzer = AstAnalyzer(file_path)
            else:
                continue

            # try some common module usage search
            modules = ['os', 'sys', 're', 'shutil', 'csv']
            for module in modules:
                nodes = analyzer.get_module_usage(module)
                # 1. `import` and `importfrom` will be included in module import usage
                # 2. `name` and `attribute` are normal usage
                # 3. `call` should be related to function call return value usage
                # 4. `str` could be module's name
                assert all(map(lambda node: isinstance(node,
                                (ast.Import, ast.ImportFrom, ast.Name, ast.Attribute, ast.Call, ast.Str)), nodes))


def test_get_module_usage_only_return_nodes_with_lineno():

    for root, dirs, files in os.walk(TEST_PACKAGE_ROOT):
        for f in files:
            file_path = os.path.join(root, f)

            two_compatible, three_compatible = True, True
            if "py2" in file_path:
                two_compatible, three_compatible = True, False
            elif "py3" in file_path:
                two_compatible, three_compatible = False, True

            if (six.PY2 and two_compatible) or ((not six.PY2) and three_compatible):
                analyzer = AstAnalyzer(file_path)
            else:
                continue

            # try some common module usage search
            modules = ['os', 're']
            for module in modules:
                nodes = analyzer.get_module_usage(module)
                assert all(map(lambda node: hasattr(node, 'lineno'), nodes))


def test_all_variables_are_name_or_attribute_nodes():

    for root, dirs, files in os.walk(TEST_PACKAGE_ROOT):
        for f in files:
            file_path = os.path.join(root, f)

            two_compatible, three_compatible = True, True
            if "py2" in file_path:
                two_compatible, three_compatible = True, False
            elif "py3" in file_path:
                two_compatible, three_compatible = False, True

            if (six.PY2 and two_compatible) or ((not six.PY2) and three_compatible):
                analyzer = AstAnalyzer(file_path)
            else:
                continue

            for _, variable_set in analyzer.variable_usage.items():
                for variable in variable_set:
                    assert isinstance(variable, (ast.Name, ast.Attribute))


def test_api_optionals_check():

    analyzer = AstAnalyzer(os.path.join(TEST_PACKAGE_ROOT, 'api_optionals_check_ACD-2725.py'))

    # lineno_only are set
    lineno_list = analyzer.get_module_usage('os', lineno_only=True)
    assert lineno_list == [1, 3]
    assert all(map(lambda lineno: isinstance(lineno, int), lineno_list))

    # use default arguments
    nodes = analyzer.get_module_usage('os')
    assert len(list(filter(lambda node: isinstance(node, ast.Import), nodes))) == 1
    assert len(list(filter(lambda node: isinstance(node, ast.Name), nodes))) == 1
    assert len(list(filter(lambda node: isinstance(node, ast.Attribute), nodes))) == 2
    assert all(map(lambda node: isinstance(node, ast.AST), nodes))

    # use with_context
    nodes = analyzer.get_module_usage('os', with_context=True)
    for node in nodes:
        # local context and global context could be None, since now I don't save context for all nodes
        assert 'ast_node' in node
        assert isinstance(node['ast_node'], ast.AST)
        assert 'local_context' in node
        assert 'global_context' in node

    # use lineno_only and with_context both, lineno_only has a higher priority
    nodes = analyzer.get_module_usage('os', lineno_only=True, with_context=True)
    assert all(map(lambda node: isinstance(node, int), nodes))


def test_api_default_return_order():

    if six.PY2:
        analyzer = AstAnalyzer(os.path.join(TEST_PACKAGE_ROOT, 'complicated_python_file_ACD-2725_py2.py'))
    else:
        analyzer = AstAnalyzer(os.path.join(TEST_PACKAGE_ROOT, 'complicated_python_file_ACD-2725_py3.py'))
    nodes = analyzer.get_module_usage('re')
    sorted_nodes = sorted(nodes, key = lambda node: node.lineno)
    assert nodes == sorted_nodes


def test_parse_python_code_with_given_context():

    context = AstContext(0, None)
    context.variable_map['a'] = AstVariable(None, {'os'})

    if six.PY2:
        analyzer = AstAnalyzer(python_file_path=os.path.join(TEST_PACKAGE_ROOT, 'parse_python_code_with_given_context_ACD-2725_py2.py'),
                           context=context)
    else:
        analyzer = AstAnalyzer(python_file_path=os.path.join(TEST_PACKAGE_ROOT, 'parse_python_code_with_given_context_ACD-2725_py3.py'),
            context=context)
    lineno_list = analyzer.get_module_usage('os', lineno_only=True)
    assert lineno_list == [1]


def test_construct_a_ast_tree():

    if six.PY2:
        python_file_path = os.path.join(TEST_PACKAGE_ROOT, 'complicated_python_file_ACD-2725_py2.py')
        analyzer = AstAnalyzer(python_file_path=python_file_path)
    else:
        python_file_path = os.path.join(TEST_PACKAGE_ROOT, 'complicated_python_file_ACD-2725_py3.py')
        analyzer = AstAnalyzer(python_file_path=python_file_path)
    # construct ast parent tree from python code
    parent_dict = {}
    queue = deque()

    queue.append(analyzer.root_ast_node)
    while queue:
        current_ast_node = queue.popleft()
        for child_node in ast.iter_child_nodes(current_ast_node):
            parent_dict[child_node] = current_ast_node
        for child_node in ast.iter_child_nodes(current_ast_node):
            queue.append(child_node)

    # compare two ast parent tree
    queue.append(analyzer.root_ast_node)
    while queue:
        current_ast_node = queue.popleft()
        # compare
        node1 , node2 = current_ast_node, current_ast_node
        while node1 and node2 and node1 == node2:
            node1 = parent_dict.get(node1, None)
            node2 = analyzer.get_parent_ast_node(node2)
        assert node1 == None and node2 == None

        for child_node in ast.iter_child_nodes(current_ast_node):
            queue.append(child_node)


def test_ast_type_components_name():

    analyzer = AstAnalyzer(python_file_path=os.path.join(TEST_PACKAGE_ROOT, 'ast_type_components_name_ACD-2725.py'))
    assert analyzer.module.name == 'ast_type_components_name_ACD-2725'
    assert analyzer.module.global_map['value'].name == 'value'
    assert analyzer.module.global_map['func'].name == 'func'
    assert analyzer.module.global_map['A'].name == 'A'


def test_assignation_with_multi_targets():

    if six.PY2:
        analyzer = AstAnalyzer(python_file_path=os.path.join(TEST_PACKAGE_ROOT, 'assignation_with_multi_target_ACD-2725_py2.py'))
    else:
        analyzer = AstAnalyzer(python_file_path=os.path.join(TEST_PACKAGE_ROOT, 'assignation_with_multi_target_ACD-2725_py3.py'))
    lineno_list = analyzer.get_module_usage('os', lineno_only=True)
    assert lineno_list == [1, 5, 6]


def test_function_yield_sensitive_module():

    if six.PY2:
        analyzer = AstAnalyzer(python_file_path=os.path.join(TEST_PACKAGE_ROOT, 'function_yield_sensitive_module_ACD-2725_py2.py'))
    else:
        analyzer = AstAnalyzer(python_file_path=os.path.join(TEST_PACKAGE_ROOT, 'function_yield_sensitive_module_ACD-2725_py3.py'))
    lineno_list = analyzer.get_module_usage('os', lineno_only=True)
    assert lineno_list == [1, 6, 7]


def test_module_used_in_assign_and_name_attribute_nodes_only():

    analyzer = AstAnalyzer(python_file_path=os.path.join(TEST_PACKAGE_ROOT, 'module_used_in_assign_and_name_attribute_nodes_only_ACD-2725.py'))
    # only `import` node will be reported
    lineno_list = analyzer.get_module_usage('os', lineno_only=True)
    assert lineno_list == [1]


def test_class_and_instance_use_isolated_namespace():

    if six.PY2:
        analyzer = AstAnalyzer(python_file_path=os.path.join(TEST_PACKAGE_ROOT, 'class_and_instance_use_isolated_namespace_ACD-2725_py2.py'))
    else:
        analyzer = AstAnalyzer(python_file_path=os.path.join(TEST_PACKAGE_ROOT, 'class_and_instance_use_isolated_namespace_ACD-2725_py3.py'))
    lineno_list = analyzer.get_module_usage('os', lineno_only=True)
    assert lineno_list == [1, 9]


def test_mixed_of_local_variable_and_class_attribute():

    if six.PY2:
        analyzer = AstAnalyzer(python_file_path=os.path.join(TEST_PACKAGE_ROOT, 'mixed_of_local_variable_and_class_attribute_ACD-2725_py2.py'))
    else:
        analyzer = AstAnalyzer(python_file_path=os.path.join(TEST_PACKAGE_ROOT, 'mixed_of_local_variable_and_class_attribute_ACD-2725_py3.py'))
    lineno_list = analyzer.get_module_usage('os', lineno_only=True)
    assert lineno_list == [1, 10]


def test_get_attribute_default_usage():

    if six.PY2:
        analyzer = AstAnalyzer(python_file_path=os.path.join(TEST_PACKAGE_ROOT, 'get_attribute_default_usage_ACD-2725_py2.py'))
    else:
        analyzer = AstAnalyzer(python_file_path=os.path.join(TEST_PACKAGE_ROOT, 'get_attribute_default_usage_ACD-2725_py3.py'))
    lineno_list = analyzer.get_module_usage('os', lineno_only=True)
    assert lineno_list == [1, 7]


def test_function_chain_is_not_variable_name():

    if six.PY2:
        analyzer = AstAnalyzer(python_file_path=os.path.join(TEST_PACKAGE_ROOT, 'function_chain_is_not_variable_name_ACD-2725_py2.py'))
    else:
        analyzer = AstAnalyzer(python_file_path=os.path.join(TEST_PACKAGE_ROOT, 'function_chain_is_not_variable_name_ACD-2725_py3.py'))
    lineno_list = analyzer.get_variable_distribution('a.b.func', lineno_only=True)
    assert lineno_list == []


def test_load_module_external_and_assign_to_local_variable():

    class ModuleManager:
        def load_modules(self, module_string):
            assert module_string == 'test'
            module = AstModule('test')
            module.global_map['func'] = AstFunction('func', None, AstVariable(None, {'os'}))
            return [module]

    if six.PY2:
        analyzer = AstAnalyzer(python_file_path=os.path.join(TEST_PACKAGE_ROOT, 'load_module_external_and_assign_to_local_variable_ACD-2725_py2.py'),
                           module_manager=ModuleManager())
    else:
        analyzer = AstAnalyzer(python_file_path=os.path.join(TEST_PACKAGE_ROOT, 'load_module_external_and_assign_to_local_variable_ACD-2725_py3.py'),
                               module_manager=ModuleManager())
    lineno_list = analyzer.get_module_usage('os', lineno_only=True)
    assert lineno_list == [4]


def test_load_function_external_and_assign_to_local_variable():

    class ModuleManager:
        def load_modules(self, module_string):
            assert module_string == 'test.func'
            func = AstFunction('func', None, AstVariable(None, {'os'}))
            return [func]

    if six.PY2:
        analyzer = AstAnalyzer(python_file_path=os.path.join(TEST_PACKAGE_ROOT, 'load_function_external_and_assign_to_local_variable_ACD-2725_py2.py'),
                           module_manager=ModuleManager())
    else:
        analyzer = AstAnalyzer(python_file_path=os.path.join(TEST_PACKAGE_ROOT, 'load_function_external_and_assign_to_local_variable_ACD-2725_py3.py'),
                               module_manager=ModuleManager())
    lineno_list = analyzer.get_module_usage('os', lineno_only=True)
    assert lineno_list == [4]


def test_load_class_external_and_assign_to_local_variable():

    class ModuleManager:
        def load_modules(self, module_string):
            assert module_string == 'test.A'
            ast_class = AstClass('A', AstContext(0 , None), function_dict={
              'func': AstFunction('func', None, AstVariable(None, {'os'}))
            })
            return [ast_class]

    if six.PY2:
        analyzer = AstAnalyzer(python_file_path=os.path.join(TEST_PACKAGE_ROOT, 'load_class_external_and_assign_to_local_variable_ACD-2725_py2.py'),
                           module_manager=ModuleManager())
    else:
        analyzer = AstAnalyzer(python_file_path=os.path.join(TEST_PACKAGE_ROOT, 'load_class_external_and_assign_to_local_variable_ACD-2725_py3.py'),
                               module_manager=ModuleManager())
    lineno_list = analyzer.get_module_usage('os', lineno_only=True)
    assert lineno_list == [4]


def test_load_external_module_with_module_manager_return_empty_list():

    class ModuleManager:
        def load_modules(self, module_string):
            assert module_string == 'os'
            return []

    if six.PY2:
        analyzer = AstAnalyzer(python_file_path=os.path.join(TEST_PACKAGE_ROOT, 'load_external_module_with_module_manager_return_empty_list_py2.py'))
    else:
        analyzer = AstAnalyzer(python_file_path=os.path.join(TEST_PACKAGE_ROOT, 'load_external_module_with_module_manager_return_empty_list_py3.py'))
    lineno_list = analyzer.get_module_usage('os', lineno_only=True)
    assert lineno_list == [1, 3, 5]

    lineno_list = analyzer.get_module_function_call_usage('os', 'fork', lineno_only=True)
    assert lineno_list == [5]


def test_load_attribute_value_external_with_module_manager_return_empty_list():

    class ModuleManager:
        def load_modules(self, module_string):
            assert module_string == 'socket.SOCK_DGRAM'
            return []

    if six.PY2:
        analyzer = AstAnalyzer(python_file_path=os.path.join(TEST_PACKAGE_ROOT, 'load_attribute_value_external_with_module_manager_return_empty_list_ACD-2725_py2.py'),
                           module_manager=ModuleManager())
    else:
        analyzer = AstAnalyzer(python_file_path=os.path.join(TEST_PACKAGE_ROOT, 'load_attribute_value_external_with_module_manager_return_empty_list_ACD-2725_py3.py'),
                               module_manager=ModuleManager())
    lineno_list = analyzer.get_module_usage('socket.SOCK_DGRAM', lineno_only=True)
    assert lineno_list == [1, 3]


def test_load_function_external_with_module_manager_return_empty_list():

    class ModuleManager:
        def load_modules(self, module_string):
            assert module_string == 'a.b'
            return []

    if six.PY2:
        analyzer = AstAnalyzer(python_file_path=os.path.join(TEST_PACKAGE_ROOT, 'load_function_external_with_module_manager_return_empty_list_ACD-2900_py2.py'),
                               module_manager=ModuleManager())
    else:
        analyzer = AstAnalyzer(python_file_path=os.path.join(TEST_PACKAGE_ROOT, 'load_function_external_with_module_manager_return_empty_list_ACD-2900_py3.py'),
                               module_manager=ModuleManager())
    lineno_list = analyzer.get_module_function_call_usage('a', 'b', lineno_only=True)
    assert lineno_list == [3]


def test_load_class_external_with_module_manager_return_empty_list():

    class ModuleManager:
        def load_modules(self, module_string):
            assert module_string == 'a.TestClass'
            return []

    if six.PY2:
        analyzer = AstAnalyzer(python_file_path=os.path.join(TEST_PACKAGE_ROOT, 'load_class_external_with_module_manager_return_empty_list_ACD-2900_py2.py'),
                           module_manager=ModuleManager())
    else:
        analyzer = AstAnalyzer(python_file_path=os.path.join(TEST_PACKAGE_ROOT, 'load_class_external_with_module_manager_return_empty_list_ACD-2900_py3.py'),
                               module_manager=ModuleManager())
    lineno_list = analyzer.get_module_function_call_usage('a', 'TestClass', lineno_only=True)
    assert lineno_list == [3]


def test_load_attribute_external_and_assign_to_local_variable():

    class ModuleManager:
        def load_modules(self, module_string):
            assert module_string == 'test.a'
            return [AstVariable(None, {'os'}, name='a')]

    if six.PY2:
        analyzer = AstAnalyzer(python_file_path=os.path.join(TEST_PACKAGE_ROOT, 'load_attribute_external_and_assign_to_local_variable_ACD-2725_py2.py'),
                           module_manager=ModuleManager())
    else:
        analyzer = AstAnalyzer(python_file_path=os.path.join(TEST_PACKAGE_ROOT, 'load_attribute_external_and_assign_to_local_variable_ACD-2725_py3.py'),
                               module_manager=ModuleManager())
    lineno_list = analyzer.get_module_usage('os', lineno_only=True)
    assert lineno_list == [4]


def test_access_self_argument_directly():

    if six.PY2:
        analyzer = AstAnalyzer(python_file_path=os.path.join(TEST_PACKAGE_ROOT, 'access_self_argument_directly_ACD-2725_py2.py'))
    else:
        analyzer = AstAnalyzer(python_file_path=os.path.join(TEST_PACKAGE_ROOT, 'access_self_argument_directly_ACD-2725_py3.py'))
    lineno_list = analyzer.get_module_usage('os', lineno_only=True)
    assert lineno_list == [1, 3, 5]


def test_self_argument_assigned_to_another_variable():

    if six.PY2:
        analyzer = AstAnalyzer(python_file_path=os.path.join(TEST_PACKAGE_ROOT, 'self_argument_assigned_to_another_variable_ACD-2725_py2.py'))
    else:
        analyzer = AstAnalyzer(python_file_path=os.path.join(TEST_PACKAGE_ROOT, 'self_argument_assigned_to_another_variable_ACD-2725_py3.py'))
    lineno_list = analyzer.get_module_usage('os', lineno_only=True)
    assert lineno_list == [1, 3, 9]


def test_self_argument_in_class_attribute():

    if six.PY2:
        analyzer = AstAnalyzer(python_file_path=os.path.join(TEST_PACKAGE_ROOT, 'self_argument_in_class_attribute_ACD-2725_py2.py'))
    else:
        analyzer = AstAnalyzer(python_file_path=os.path.join(TEST_PACKAGE_ROOT, 'self_argument_in_class_attribute_ACD-2725_py3.py'))
    lineno_list = analyzer.get_module_usage('os', lineno_only=True)
    assert lineno_list == [1, 7]


def test_class_attribute_named_self():

    if six.PY2:
        analyzer = AstAnalyzer(python_file_path=os.path.join(TEST_PACKAGE_ROOT, 'class_attribute_named_self_ACD-2725_py2.py'))
    else:
        analyzer = AstAnalyzer(python_file_path=os.path.join(TEST_PACKAGE_ROOT, 'class_attribute_named_self_ACD-2725_py3.py'))
    lineno_list = analyzer.get_module_usage('os', lineno_only=True)
    assert lineno_list == [1, 6]


def test_assign_self_to_another_class_attribute_in_global_class():

    if six.PY2:
        analyzer = AstAnalyzer(python_file_path=os.path.join(TEST_PACKAGE_ROOT, 'assign_self_to_another_class_attribute_in_global_class_ACD-2725_py2.py'))
    else:
        analyzer = AstAnalyzer(python_file_path=os.path.join(TEST_PACKAGE_ROOT, 'assign_self_to_another_class_attribute_in_global_class_ACD-2725_py3.py'))
    lineno_list = analyzer.get_module_usage('os', lineno_only=True)
    assert lineno_list == [6, 10]


def test_assign_self_to_another_class_attribute_in_local_class():

    if six.PY2:
        analyzer = AstAnalyzer(python_file_path=os.path.join(TEST_PACKAGE_ROOT, 'assign_self_to_another_class_attribute_in_local_class_ACD-2725_py2.py'))
    else:
        analyzer = AstAnalyzer(python_file_path=os.path.join(TEST_PACKAGE_ROOT, 'assign_self_to_another_class_attribute_in_local_class_ACD-2725_py3.py'))
    lineno_list = analyzer.get_module_usage('os', lineno_only=True)
    assert lineno_list == [7, 11]


def test_interesting_module_alias_and_assignation():

    if six.PY2:
        analyzer = AstAnalyzer(python_file_path=os.path.join(TEST_PACKAGE_ROOT, 'interesting_module_alias_and_assignation_ACD-2725_py2.py'))
    else:
        analyzer = AstAnalyzer(python_file_path=os.path.join(TEST_PACKAGE_ROOT, 'interesting_module_alias_and_assignation_ACD-2725_py3.py'))
    lineno_list = analyzer.get_module_usage('os', lineno_only=True)
    assert lineno_list == [6, 8]

    # line 8 is false positive, but it is by design
    lineno_list = analyzer.get_module_usage('sys', lineno_only=True)
    assert lineno_list == [1, 8]


def test_variable_usage_in_base_class():

    analyzer = AstAnalyzer(python_file_path=os.path.join(TEST_PACKAGE_ROOT, 'variable_usage_in_base_class_ACD-2725.py'))
    lineno_list = analyzer.get_variable_distribution('a.b', lineno_only=True)
    assert lineno_list == [1]

    lineno_list = analyzer.get_variable_distribution('a', lineno_only=True)
    assert lineno_list == [1]

    lineno_list = analyzer.get_variable_distribution('a.b.c', lineno_only=True)
    assert lineno_list == []


def test_variable_distribution_usage_corner_case():

    if six.PY2:
        analyzer = AstAnalyzer(python_file_path=os.path.join(TEST_PACKAGE_ROOT, 'variable_distribution_usage_corner_case_ACD-2845_py2.py'))
    else:
        analyzer = AstAnalyzer(python_file_path=os.path.join(TEST_PACKAGE_ROOT, 'variable_distribution_usage_corner_case_ACD-2845_py3.py'))

    # complicated function call
    lineno_list = analyzer.get_variable_distribution('a.b.c', lineno_only=True)
    assert lineno_list == []

    # function argument
    lineno_list = analyzer.get_variable_distribution('value', lineno_only=True)
    assert lineno_list == [3]

    # simple function call
    lineno_list = analyzer.get_variable_distribution('func', lineno_only=True)
    assert lineno_list == []


def test_only_assign_variable_to_function_modules():

    analyzer = AstAnalyzer(python_file_path=os.path.join(TEST_PACKAGE_ROOT, 'only_assign_variable_to_function_modules_ACD-2845.py'))

    function_call_nodes = analyzer.get_module_function_call_usage('socket', 'socket', fuzzy=True)
    assert len(function_call_nodes) == 4

    query = analyzer.query().call_nodes(force_propagate = False)
    while not query.is_end():
        query.call_nodes(force_propagate = False)

    result = query.filter(Any(analyzer.get_module_function_call_usage('socket', 'socket'))) \
                  .filter(Any(analyzer.get_module_usage('socket.AF_INET'))) \
                  .filter(Any(analyzer.get_module_usage('socket.SOCK_DGRAM'))).collect()

    assert len(result) == 2
    result.sort(key = lambda node: node.lineno)
    assert (result[0].lineno, result[1].lineno) == (3, 5)


def test_analyzer_memory_usage_with_so_many_name_nodes():

    memory_unit = 1000 * 1000
    analyzer = AstAnalyzer(python_file_path=os.path.join(TEST_PACKAGE_ROOT,
                                                         'high_memory_usage_python_file_with_so_many_name_nodes_ACD-2861.py'))
    # expected value: 66136888, may add more features in the future, it could be bigger
    assert asizeof.asizeof(analyzer) <= 70 * memory_unit


def test_analyzer_memory_usage_with_so_many_attribute_nodes():

    memory_unit = 1000 * 1000
    analyzer = AstAnalyzer(python_file_path=os.path.join(TEST_PACKAGE_ROOT,
                                                         'high_memory_usage_python_file_with_so_many_attribute_nodes_ACD-2861.py'))
    # expected value: 21013416, may add more features in the future, it could be bigger
    assert asizeof.asizeof(analyzer) <= 25 * memory_unit


def test_class_method_call_in_fuzzy_and_exactly_mode():

    if six.PY2:
        analyzer = AstAnalyzer(python_file_path=os.path.join(TEST_PACKAGE_ROOT,
                                                        'class_method_call_in_fuzzy_and_exactly_mode_ACD-2416_py2.py'))
    else:
        analyzer = AstAnalyzer(python_file_path=os.path.join(TEST_PACKAGE_ROOT,
                                                             'class_method_call_in_fuzzy_and_exactly_mode_ACD-2416_py3.py'))
    lineno_list = analyzer.get_module_function_call_usage('socket', 'socket', lineno_only=True)
    assert lineno_list == []

    lineno_list = analyzer.get_module_function_call_usage('socket', 'socket', lineno_only=True, fuzzy=True)
    assert lineno_list == [5]


def test_function_call_in_fuzzy_and_exactly_mode():

    analyzer = AstAnalyzer(python_file_path=os.path.join(TEST_PACKAGE_ROOT,
                                                         'function_call_in_fuzzy_and_exactly_mode_ACD-2416.py'))
    lineno_list = analyzer.get_module_function_call_usage('socket', 'socket', lineno_only=True)
    assert lineno_list == [4, 6]

    lineno_list = analyzer.get_module_function_call_usage('socket', 'socket', lineno_only=True, fuzzy=True)
    assert lineno_list == [3, 4, 6]


def test_class_method_call_in_class_method_call_with_useless_return_value():

    analyzer = AstAnalyzer(python_file_path=os.path.join(TEST_PACKAGE_ROOT,
                                                        'class_method_call_in_class_method_call_with_useless_return_value_ACD-2416.py'))
    lineno_list = analyzer.get_module_function_call_usage('socket', 'socket', lineno_only=True)
    assert lineno_list == []

    lineno_list = analyzer.get_module_function_call_usage('socket', 'socket', lineno_only=True, fuzzy=True)
    assert lineno_list == []


def test_class_method_call_in_class_method_call_with_useful_return_value():

    if six.PY2:
        analyzer = AstAnalyzer(python_file_path=os.path.join(TEST_PACKAGE_ROOT,
                                                         'class_method_call_in_class_method_call_with_useful_return_value_ACD-2416_py2.py'))
    else:
        analyzer = AstAnalyzer(python_file_path=os.path.join(TEST_PACKAGE_ROOT,
                                                             'class_method_call_in_class_method_call_with_useful_return_value_ACD-2416_py3.py'))
    lineno_list = analyzer.get_module_function_call_usage('socket', 'socket', lineno_only=True)
    assert lineno_list == [7]

    lineno_list = analyzer.get_module_function_call_usage('socket', 'socket', lineno_only=True, fuzzy=True)
    assert lineno_list == [7]


def test_class_method_return_risk_module_chain():

    if six.PY2:
        analyzer = AstAnalyzer(python_file_path=os.path.join(TEST_PACKAGE_ROOT,
                                                        'class_method_return_risk_module_chain_ACD-2416_py2.py'))
    else:
        analyzer = AstAnalyzer(python_file_path=os.path.join(TEST_PACKAGE_ROOT,
                                                             'class_method_return_risk_module_chain_ACD-2416_py3.py'))

    lineno_list = analyzer.get_module_function_call_usage('socket', 'socket', lineno_only=True)
    assert lineno_list == [8]

    lineno_list = analyzer.get_module_function_call_usage('socket', 'socket', lineno_only=True, fuzzy=True)
    assert lineno_list == [8]


def test_assign_variable_with_function_call_return_value():

    analyzer = AstAnalyzer(python_file_path=os.path.join(TEST_PACKAGE_ROOT,
                                                         'assign_variable_with_function_call_return_value_ACD-2416.py'))
    lineno_list = analyzer.get_module_function_call_usage('socket', 'socket', lineno_only=True)
    assert lineno_list == [7]

    lineno_list = analyzer.get_module_function_call_usage('socket', 'socket', lineno_only=True, fuzzy=True)
    assert lineno_list == [7, 10]


def test_assign_variable_with_weird_function_call_return_value():

    if six.PY2:
        analyzer = AstAnalyzer(python_file_path=os.path.join(TEST_PACKAGE_ROOT,
                                                         'assign_variable_with_weird_function_call_return_value_ACD-2416_py2.py'))
    else:
        analyzer = AstAnalyzer(python_file_path=os.path.join(TEST_PACKAGE_ROOT,
                                                             'assign_variable_with_weird_function_call_return_value_ACD-2416_py3.py'))
    # In line number four and five, variable won't be assigned to socket.socket type
    lineno_list = analyzer.get_module_usage('socket.socket', lineno_only=True)
    assert lineno_list == [7, 8]


def test_assign_variable_with_risk_arguments():

    if six.PY2:
        analyzer = AstAnalyzer(python_file_path=os.path.join(TEST_PACKAGE_ROOT,
                                                         'assign_variable_with_risk_arguments_ACD-2416_py2.py'))
    else:
        analyzer = AstAnalyzer(python_file_path=os.path.join(TEST_PACKAGE_ROOT,
                                                             'assign_variable_with_risk_arguments_ACD-2416_py3.py'))
    # By design, arguments' type won't be assigned to target variable
    lineno_list = analyzer.get_module_usage('os', lineno_only=True)
    assert lineno_list == [1, 3]

    # No `os` function call would be detected, since arguments won't be collected
    lineno_list = analyzer.get_module_function_call_usage('os', lineno_only=True, fuzzy=True)
    assert lineno_list == []


def test_load_module_from_metadata_extension():

    class PythonFunction(AstCallableFunction):
        def __init__(self):
            AstCallableFunction.__init__(self, 'join')

        def action(self, function_node, analyzer, args, keywords, context):
            # Delegate function call procedure to python function object
            # Keep user defined function simple, only args and keywords are required positional arguments
            # other arguments are optional keyword arguments
            if args:
                # only when all arguments are ready, concatenate all strings together
                for arg in args:
                    if not AstVariable.is_string(arg):
                        return AstVariable(None, {AstVariable.STRING_TYPE}, '?')
                root_path = args[0].variable_value
                paths = [arg.variable_value for arg in args[1:]]
                return AstVariable(None, {AstVariable.STRING_TYPE}, os.path.join(root_path, *paths))
            else:
                return AstVariable(None, {AstVariable.STRING_TYPE}, '')

    class ModuleManager:
        def load_modules(self, module_string):
            assert module_string == 'os'
            # load os module
            os_module = AstModule('os')
            path_module = AstModule('path')
            os_module.global_map['path'] = path_module
            path_module.global_map['join'] = PythonFunction()
            return [os_module]

    analyzer = AstAnalyzer(python_file_path=os.path.join(TEST_PACKAGE_ROOT, 'load_module_from_metadata_extension_ACD-2900.py'),
                           module_manager=ModuleManager())
    variable = analyzer.get_variable_details(analyzer.get_variable_distribution('result')[0])
    assert AstVariable.is_string(variable)
    assert variable.variable_value == os.path.join('a', 'b', 'c')

    unknown_variable = analyzer.get_variable_details(analyzer.get_variable_distribution('unknown_result')[0])
    assert AstVariable.is_string(unknown_variable)
    assert unknown_variable.variable_value == '?'


def test_load_function_from_metadata_extension():

    '''
    os.path.join function implementation
    '''
    class PythonFunction(AstCallableFunction):
        def __init__(self):
            AstCallableFunction.__init__(self, 'join')

        def action(self, function_node, analyzer, args, keywords, context):
            # Delegate function call procedure to python function object
            # Keep user defined function simple, only args and keywords are required positional arguments
            # other arguments are optional keyword arguments
            if args:
                # only when all arguments are ready, concatenate all strings together
                for arg in args:
                    if not AstVariable.is_string(arg):
                        return AstVariable(None, {AstVariable.STRING_TYPE}, '?')
                root_path = args[0].variable_value
                paths = [arg.variable_value for arg in args[1:]]
                return AstVariable(None, {AstVariable.STRING_TYPE}, os.path.join(root_path, *paths))
            else:
                return AstVariable(None, {AstVariable.STRING_TYPE}, '')

    class ModuleManager:
        def load_modules(self, module_string):
            assert module_string == 'os.path.join'
            # load os.path.join function
            return [PythonFunction()]

    analyzer = AstAnalyzer(python_file_path=os.path.join(TEST_PACKAGE_ROOT, 'load_function_from_metadata_extension_ACD-2900.py'),
                           module_manager=ModuleManager())
    variable = analyzer.get_variable_details(analyzer.get_variable_distribution('result')[0])
    assert AstVariable.is_string(variable)
    assert variable.variable_value == os.path.join('hello', 'world')

    unknown_variable = analyzer.get_variable_details(analyzer.get_variable_distribution('unknown_result')[0])
    assert AstVariable.is_string(unknown_variable)
    assert unknown_variable.variable_value == '?'


def test_load_class_from_metadata_external_extension():

    class ModuleManager:
        def load_modules(self, module_string):
            assert module_string == 'a.Test'
            ast_class = AstClass('Test', AstContext(0, None), modules={'os'})
            return [ast_class]

    if six.PY2:
        analyzer = AstAnalyzer(python_file_path=os.path.join(TEST_PACKAGE_ROOT, 'load_class_from_metadata_external_extension_ACD-2900_py2.py'),
                           module_manager = ModuleManager())
    else:
        analyzer = AstAnalyzer(python_file_path=os.path.join(TEST_PACKAGE_ROOT, 'load_class_from_metadata_external_extension_ACD-2900_py3.py'),
                           module_manager=ModuleManager())
    result_list = analyzer.get_module_function_call_usage('os', lineno_only=True)
    assert result_list == [3]
    result_list = analyzer.get_module_function_call_usage('os', 'test', lineno_only=True)
    assert result_list == [4]


def test_load_variable_from_metadata_external_extension():

    class ModuleManager:
        def load_modules(self, module_string):
            assert module_string == 'a.b'
            ast_variable = AstVariable(None, {'os'}, name='b')
            return [ast_variable]

    if six.PY2:
        analyzer = AstAnalyzer(python_file_path=os.path.join(TEST_PACKAGE_ROOT, 'load_variable_from_metadata_external_extension_ACD-2900_py2.py'),
                           module_manager=ModuleManager())
    else:
        analyzer = AstAnalyzer(python_file_path=os.path.join(TEST_PACKAGE_ROOT, 'load_variable_from_metadata_external_extension_ACD-2900_py3.py'),
                               module_manager=ModuleManager())
    result_list = analyzer.get_module_usage('os', lineno_only=True)
    assert result_list == [3]


def test_load_module_from_external_extension_but_without_necessary_stuff():

    '''
    extension only return os module and without any details, but analyzer should still handle this situation
    '''
    class ModuleManager:
        def load_modules(self, module_string):
            assert module_string == 'os'
            ast_module = AstModule('os', namespace='os')
            return [ast_module]

    if six.PY2:
        analyzer = AstAnalyzer(python_file_path=os.path.join(TEST_PACKAGE_ROOT, 'load_module_from_metadata_external_extension_but_without_necessary_stuff_ACD-2900_py2.py'),
                           module_manager=ModuleManager())
    else:
        analyzer = AstAnalyzer(python_file_path=os.path.join(TEST_PACKAGE_ROOT, 'load_module_from_metadata_external_extension_but_without_necessary_stuff_ACD-2900_py3.py'),
                               module_manager=ModuleManager())
    result_list = analyzer.get_module_function_call_usage('os', 'fork', lineno_only=True)
    assert result_list == [3]

    result_list = analyzer.get_module_function_call_usage('os', 'join', lineno_only=True, fuzzy=True)
    assert result_list == [5, 9]


def test_load_module_from_metadata_external_extension_with_partial_information():

    class ModuleManager:
        def load_modules(self, module_string):
            assert module_string == 'os'
            os_module = AstModule('os', namespace='os')
            path_module = AstModule('path', namespace='os.path')
            os_module.global_map['path'] = path_module
            return [os_module]

    if six.PY2:
        analyzer = AstAnalyzer(python_file_path=os.path.join(TEST_PACKAGE_ROOT, 'load_module_from_metadata_external_extension_with_partial_information_ACD-2900_py2.py'),
                           module_manager=ModuleManager())
    else:
        analyzer = AstAnalyzer(python_file_path=os.path.join(TEST_PACKAGE_ROOT, 'load_module_from_metadata_external_extension_with_partial_information_ACD-2900_py3.py'),
                               module_manager=ModuleManager())
    result_list = analyzer.get_module_usage('os', lineno_only=True)
    assert result_list == [1, 3, 4]


def test_callable_function_usage():

    class PythonFunction(AstCallableFunction):

        def __init__(self, name):
            AstCallableFunction.__init__(self, name)

        def action(self, function_node, analyzer, args, keywords, context):
            return AstVariable(None, {'os'})

    class ModuleManager:
        def load_modules(self, module_string):
            assert module_string == 'a.func'
            return [PythonFunction('func')]

    if six.PY2:
        analyzer = AstAnalyzer(python_file_path=os.path.join(TEST_PACKAGE_ROOT, 'callable_function_usage_ACD-2900_py2.py'),
                           module_manager=ModuleManager())
    else:
        analyzer = AstAnalyzer(python_file_path=os.path.join(TEST_PACKAGE_ROOT, 'callable_function_usage_ACD-2900_py3.py'),
                               module_manager=ModuleManager())
    result_list = analyzer.get_module_function_call_usage('os', 'test', lineno_only=True)
    assert result_list == [4, 9]

    # check result and another_result
    result_ast_node = analyzer.get_variable_distribution('result')[0]
    another_result_ast_node = analyzer.get_variable_distribution('another_result')[0]

    result_variable = analyzer.get_variable_details(result_ast_node)
    another_result_variable = analyzer.get_variable_details(another_result_ast_node)

    assert result_variable.variable_type_set == {'os'}
    assert another_result_variable.variable_type_set == {'os'}


def test_callable_function_chain_usage():

    class FuncFunction(AstCallableFunction):

        def __init__(self, name):
            AstCallableFunction.__init__(self, name)

        def action(self, function_node, analyzer, args, keywords, context):
            return TestFunction('test')

    class TestFunction(AstCallableFunction):

        def __init__(self, name):
            AstCallableFunction.__init__(self, name)

        def action(self, function_node, analyzer, args, keywords, context):
            return AstVariable(None, {'os'})

    class ModuleManager:

        def load_modules(self, module_string):
            assert module_string == 'a.func'
            return [FuncFunction('func')]

    analyzer = AstAnalyzer(python_file_path=os.path.join(TEST_PACKAGE_ROOT, 'callable_function_chain_usage_ACD-2900.py'),
                           module_manager=ModuleManager())

    # check result's value
    ast_variable = analyzer.get_variable_distribution('result')[0]
    assert analyzer.get_variable_details(ast_variable).variable_type_set == {'os'}


def test_module_function_call_usage_only_return_module_function_call():

    if six.PY2:
        analyzer = AstAnalyzer(python_file_path=os.path.join(TEST_PACKAGE_ROOT, 'module_function_call_usage_only_return_module_function_call_ACD-2900_py2.py'))
    else:
        analyzer = AstAnalyzer(python_file_path=os.path.join(TEST_PACKAGE_ROOT, 'module_function_call_usage_only_return_module_function_call_ACD-2900_py3.py'))

    result_list = analyzer.get_module_function_call_usage('os', fuzzy=True)
    # now line number six is not sensitive
    result_list.sort(key = lambda node: node.lineno)
    assert len(result_list) == 3

    assert result_list[0].func.attr == 'join'
    assert result_list[0].lineno == 8

    assert result_list[1].func.attr == 'join'
    assert result_list[1].lineno == 12

    assert result_list[2].func.id == 'os'
    assert result_list[2].lineno == 14


def test_mix_of_function_call_callable_function_call():

    class PythonFunction(AstCallableFunction):

        def __init__(self, name):
            AstCallableFunction.__init__(self, name)

        def action(self, function_node, analyzer, args, keywords, context):
            return AstVariable(None, {'os'})

    class ModuleManager:
        def load_modules(self, module_string):
            assert module_string == 'a.func'
            return [PythonFunction('func')]

    if six.PY2:
        analyzer = AstAnalyzer(python_file_path=os.path.join(TEST_PACKAGE_ROOT, 'mix_of_function_call_callable_function_call_ACD-2900_py2.py'),
                           module_manager=ModuleManager())
    else:
        analyzer = AstAnalyzer(python_file_path=os.path.join(TEST_PACKAGE_ROOT, 'mix_of_function_call_callable_function_call_ACD-2900_py3.py'),
            module_manager=ModuleManager())
    assert analyzer.get_module_usage('os', lineno_only=True) == [6]
    assert analyzer.get_module_function_call_usage('os', lineno_only=True, fuzzy=True) == []


def test_call_node_modules_with_module_manager_return_some_info():

    class ModuleManager:
        def load_modules(self, module_string):
            assert module_string == 'os'
            os_module = AstModule('os', namespace='os')
            os_module.global_map['path'] = AstModule('path', namespace='os.path')
            return [os_module]

    if six.PY2:
        analyzer = AstAnalyzer(python_file_path=os.path.join(TEST_PACKAGE_ROOT, 'call_node_modules_with_module_manager_return_some_info_ACD-2900_py2.py'),
                           module_manager=ModuleManager())
    else:
        analyzer = AstAnalyzer(python_file_path=os.path.join(TEST_PACKAGE_ROOT, 'call_node_modules_with_module_manager_return_some_info_ACD-2900_py3.py'),
                               module_manager=ModuleManager())
    for node in ast.walk(analyzer.root_ast_node):
        if isinstance(node, ast.Call):
            # all possible prefix are collected
            assert analyzer.get_call_node_modules(node) == {'os', 'os.path', 'os.path.join'}


def test_module_manager_return_correct_module_but_without_required_function():

    class ModuleManager:
        def load_modules(self, module_string):
            assert module_string == 'os'
            os_module = AstModule('os', namespace='os')
            os_module.global_map['path'] = AstModule('path', namespace='os.path')
            return [os_module]

    if six.PY2:
        analyzer = AstAnalyzer(python_file_path=os.path.join(TEST_PACKAGE_ROOT, 'module_manager_return_correct_module_but_without_required_function_ACD-2900_py2.py'),
                           module_manager=ModuleManager())
    else:
        analyzer = AstAnalyzer(python_file_path=os.path.join(TEST_PACKAGE_ROOT, 'module_manager_return_correct_module_but_without_required_function_ACD-2900_py3.py'),
                               module_manager=ModuleManager())

    lineno_list = analyzer.get_module_function_call_usage('os.path', 'join', lineno_only=True)
    assert lineno_list == [3]


def test_module_manager_return_correct_function():

    class PythonFunction(AstCallableFunction):

        def __init__(self, name, namespace):
            AstCallableFunction.__init__(self, name, namespace)

        def action(self, function_node, analyzer, args, keywords, context):
            return AstVariable(None, {AstVariable.STRING_TYPE}, variable_value='for test')

    class ModuleManager:

        def load_modules(self, module_string):
            assert module_string == 'os.path.join'
            return [PythonFunction('join', 'os.path.join')]

    analyzer = AstAnalyzer(python_file_path=os.path.join(TEST_PACKAGE_ROOT, 'module_manager_return_correct_function_ACD-2900.py'),
                           module_manager=ModuleManager())
    lineno_list = analyzer.get_module_function_call_usage('os.path', 'join', lineno_only=True)
    assert lineno_list == [3]

    ast_node = analyzer.get_variable_distribution('result')[0]
    variable = analyzer.get_variable_details(ast_node)
    assert variable.variable_value == 'for test'


def test_load_class_from_external_and_inherit_from_that_class():

    class ModuleManager:
        def load_modules(self, module_string):
            assert module_string == 'asyncore'
            ast_context = AstContext(0 , None)
            ast_class = AstClass('dispatcher', ast_context, namespace='asyncore.dispatcher')
            ast_module = AstModule('asyncore', namespace='asyncore')
            ast_module.global_map['dispatcher'] = ast_class
            return [ast_module]

    analyzer = AstAnalyzer(python_file_path=os.path.join(TEST_PACKAGE_ROOT, 'load_class_from_external_and_inherit_from_that_class_ACD-1797.py'),
                           module_manager=ModuleManager())
    lineno_list = analyzer.get_module_usage('asyncore.dispatcher', lineno_only=True)
    assert lineno_list == [3]

    lineno_list = analyzer.get_module_usage('asyncore', lineno_only=True)
    assert lineno_list == [1, 3]


def test_load_submodule_from_external():

    class ModuleManager:
        def load_modules(self, module_string):
            assert module_string == 'os.path'
            path_module = AstModule('path', namespace='os.path')
            return [path_module]

    analyzer = AstAnalyzer(python_file_path=os.path.join(TEST_PACKAGE_ROOT, 'load_submodule_from_external_ACD-1797.py'),
                           module_manager=ModuleManager())
    lineno_list = analyzer.get_module_usage('os.path', lineno_only=True)
    assert lineno_list == [1]

    lineno_list = analyzer.get_module_usage('os', lineno_only=True)
    assert lineno_list == [1]

def test_builtin_module_import_open():

    if six.PY2:
        analyzer = AstAnalyzer(python_file_path=os.path.join(TEST_PACKAGE_ROOT, 'builtin_module_import_open_ACD-1806_py2.py'))
    else:
        analyzer = AstAnalyzer(python_file_path=os.path.join(TEST_PACKAGE_ROOT, 'builtin_module_import_open_ACD-1806_py3.py'))

    lineno_list = analyzer.get_module_function_call_usage(AstVariable.BUILTIN_TYPE, 'open', lineno_only=True)
    assert lineno_list == [3]

    lineno_list = analyzer.get_module_function_call_usage('file', 'read', lineno_only=True)
    assert lineno_list == [4]

    lineno_list = analyzer.get_module_function_call_usage('file', 'write', lineno_only=True)
    assert lineno_list == [5]


def test_builtin_module_import_eval():

    if six.PY2:
        analyzer = AstAnalyzer(python_file_path=os.path.join(TEST_PACKAGE_ROOT, 'builtin_module_import_eval_ACD-1806_py2.py'))
    else:
        analyzer = AstAnalyzer(python_file_path=os.path.join(TEST_PACKAGE_ROOT, 'builtin_module_import_eval_ACD-1806_py3.py'))

    lineno_list = analyzer.get_module_function_call_usage(AstVariable.BUILTIN_TYPE, 'eval', lineno_only=True)
    assert lineno_list == [6]

    os_module = analyzer.get_variable_distribution('os_module')[0]
    module_variable = analyzer.get_variable_details(os_module)
    assert module_variable.variable_type_set == {'os'}


def test_default_builtins_module_usage():

    analyzer = AstAnalyzer(python_file_path=os.path.join(TEST_PACKAGE_ROOT, 'default_builtins_module_usage_ACD-1806.py'))

    lineno_list = analyzer.get_module_function_call_usage(AstVariable.BUILTIN_TYPE, 'open', lineno_only=True)
    assert lineno_list == [1]

    lineno_list = analyzer.get_module_function_call_usage('file', 'write', lineno_only=True)
    assert lineno_list == [3]

    lineno_list = analyzer.get_module_function_call_usage('file', 'read', lineno_only=True)
    assert lineno_list == [4]

    ast_node = analyzer.get_variable_distribution('value')[0]
    variable = analyzer.get_variable_details(ast_node)
    assert variable.variable_type_set == {AstVariable.STRING_TYPE}
    assert variable.variable_value == 'hello'


def test_double_open_in_with_statement():

    analyzer = AstAnalyzer(python_file_path=os.path.join(TEST_PACKAGE_ROOT, 'double_open_in_with_statement_ACD-1795.py'))

    lineno_list = analyzer.get_module_function_call_usage(AstVariable.BUILTIN_TYPE, 'open', lineno_only=True)
    assert lineno_list == [3]

    lineno_list = analyzer.get_module_function_call_usage('gzip', 'open', lineno_only=True)
    assert lineno_list == [3]


def test_with_statement_with_tuple_target():

    analyzer = AstAnalyzer(python_file_path=os.path.join(TEST_PACKAGE_ROOT, 'with_statement_with_tuple_target_ACD-3129.py'))

    lineno_list = analyzer.get_module_function_call_usage('os', 'open', lineno_only=True, fuzzy=True)
    assert lineno_list == [3, 4, 5]


def test_super_class_usage():

    if six.PY2:
        analyzer = AstAnalyzer(python_file_path=os.path.join(TEST_PACKAGE_ROOT, "super_class_usage_ACD-3243_py2.py"))
    else:
        analyzer = AstAnalyzer(python_file_path=os.path.join(TEST_PACKAGE_ROOT, "super_class_usage_ACD-3243_py3.py"))

    lineno_list = analyzer.get_module_function_call_usage("requests.Session", "request", lineno_only=True)
    assert lineno_list == [53]


def test_builtin_apply_usage():

    if six.PY2:
        analyzer = AstAnalyzer(python_file_path=os.path.join(TEST_PACKAGE_ROOT, "builtin_apply_usage_py2.py"))
    else:
        analyzer = AstAnalyzer(python_file_path=os.path.join(TEST_PACKAGE_ROOT, "builtin_apply_usage_py3.py"))

    lineno_list = analyzer.get_module_function_call_usage("os.path", lineno_only=True)
    assert lineno_list == [3]

    lineno_list = analyzer.get_module_function_call_usage("os", lineno_only=True)
    assert lineno_list == [3]