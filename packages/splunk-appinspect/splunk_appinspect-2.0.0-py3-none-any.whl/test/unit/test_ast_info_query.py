from splunk_appinspect.python_analyzer.ast_analyzer import AstAnalyzer
from splunk_appinspect.python_analyzer.ast_info_query import MultiAnd, MultiOr, And, Or, Any, All

import os
import ast
import six

TEST_PACKAGE_ROOT = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'python_analyzer_packages', 'ast_info_query_python_files')


def test_create_isolated_query():

    if six.PY2:
        analyzer = AstAnalyzer(python_code_string='print "sdfsd"')
    else:
        analyzer = AstAnalyzer(python_code_string="print('sdfsd')")
    query1 = analyzer.query()
    query2 = analyzer.query()
    assert id(query1) != id(query2)


def test_call_nodes_force_propagate():

    analyzer = AstAnalyzer(os.path.join(TEST_PACKAGE_ROOT, 'call_nodes_propagate_ACD-2845.py'))
    query = analyzer.query().call_nodes()

    call_nodes = set()
    layer = 0

    while not query.is_end():
        nodes = list(query.collect())

        if layer == 0:
            assert len(nodes) == 1
            assert nodes[0].func.attr == 'socket'
        elif layer == 1:
            assert len(nodes) == 2
            assert (nodes[0].func.id == 'func1' and nodes[1].func.id == 'func2')
        else:
            assert False

        for node in nodes:
            call_nodes.add(node)

        query.call_nodes()
        layer += 1

    assert len(call_nodes) == 3
    assert all(map(lambda node: isinstance(node, ast.Call), call_nodes))
    assert all(map(lambda node: node.lineno == 9, call_nodes))


def test_call_nodes_propagate():

    analyzer = AstAnalyzer(os.path.join(TEST_PACKAGE_ROOT, 'call_nodes_propagate_ACD-2845.py'))
    query = analyzer.query().call_nodes()

    layer = 0
    while not query.is_end():
        layer += 1
        if layer == 1:
            assert len(query.collect()) == 1
            assert query.collect()[0].func.attr == 'socket'
        elif layer == 2:
            assert len(query.collect()) == 2
            functions = query.collect()
            functions.sort(key = lambda node: node.func.id)
            assert (functions[0].func.id, functions[1].func.id) == ('func1', 'func2')
        query.call_nodes(force_propagate = False)

    functions = query.collect()
    assert len(functions) == 2
    functions.sort(key = lambda node: node.func.id)
    assert (functions[0].func.id, functions[1].func.id) == ('func1', 'func2')


def test_force_propagate_feature():

    analyzer = AstAnalyzer(os.path.join(TEST_PACKAGE_ROOT, 'call_nodes_propagate_ACD-2845.py'))
    query = analyzer.query()

    # total number of ast node
    total , need = 0 , 0
    while not query.is_end():
        total += len(query.collect())
        query.propagate_nodes()

    for _ in ast.walk(analyzer.root_ast_node):
        need += 1
    assert total == need

    # total number of call nodes
    total , need = 0 , 0
    query.reset()
    query.call_nodes()
    while not query.is_end():
        total += len(query.collect())
        query.call_nodes()

    for node in ast.walk(analyzer.root_ast_node):
        if isinstance(node, ast.Call):
            need += 1
    assert total == need


def test_propagate_feature():

    analyzer = AstAnalyzer(os.path.join(TEST_PACKAGE_ROOT, 'nested_class_nodes_ACD-2845.py'))
    query = analyzer.query()

    # check total number of nodes
    need_set = set()
    for node in ast.walk(analyzer.root_ast_node):
        need_set.add(node)

    # the initial value is one, since Ast.Module will always be included
    total_set = {analyzer.root_ast_node}
    query.propagate_nodes(force_propagate = False)
    while not query.is_end():
        total_set |= set(query.collect())
        query.propagate_nodes(force_propagate = False)

    assert len(total_set) == len(need_set)


def test_multi_stages_force_propagate():

    analyzer = AstAnalyzer(os.path.join(TEST_PACKAGE_ROOT, 'call_nodes_propagate_ACD-2845.py'))
    query = analyzer.query()
    # module always be the first node
    nodes = query.collect()
    assert len(nodes) == 1
    assert isinstance(nodes[0], ast.Module)

    # first phase
    query.function_nodes()
    functions = query.collect()
    assert len(functions) == 2
    assert functions[0].name == 'func1'
    assert functions[1].name == 'func2'

    # second phase
    query.attribute_nodes()
    attributes = query.collect()

    assert len(attributes) == 2
    assert attributes[0].attr == 'AF_INET'
    assert attributes[1].attr == 'SOCK_DGRAM'

    # third phase
    query.name_nodes()
    names = query.collect()
    assert len(names) == 2
    assert names[0].id == 'socket'
    assert names[1].id == 'socket'

    # try to propagate again...
    # Some ctx nodes still exist
    query.propagate_nodes()
    assert query.is_end() == False
    assert all(map(lambda node: isinstance(node, ast.Load), query.collect()))

    # try again...
    query.propagate_nodes()
    assert query.is_end() == True

    # try once more...
    query.propagate_nodes()
    assert query.is_end() == True


def test_multi_stages_propagate():

    analyzer = AstAnalyzer(os.path.join(TEST_PACKAGE_ROOT, 'multi_stages_propagate_ACD-2845.py'))
    query = analyzer.query()

    query.class_nodes(force_propagate = False)

    query.function_nodes(force_propagate = False)
    while not query.is_end():
        query.function_nodes(force_propagate = False)

    query.call_nodes(force_propagate = False)
    while not query.is_end():
        query.call_nodes(force_propagate = False)

    nodes1 = analyzer.get_module_function_call_usage('socket', 'socket')
    nodes2 = analyzer.get_module_usage('socket.AF_INET')
    nodes3 = analyzer.get_module_usage('socket.SOCK_DGRAM')

    query.filter(Any(nodes1)).filter(Any(nodes2)).filter(Any(nodes3))
    assert len(query.collect()) == 3


def test_force_propagate_and_propagate_difference_in_corner_cases():

    analyzer = AstAnalyzer(os.path.join(TEST_PACKAGE_ROOT, 'nested_class_nodes_ACD-2845.py'))
    query1 = analyzer.query()
    query2 = query1.persist()

    for _ in range(3):
        query1.call_nodes()
        query2.call_nodes(force_propagate = False)

    assert len(query1.collect()) == 0
    assert len(query2.collect()) == 2

    assert all(map(lambda node: node.func.attr == 'socket', query2.collect()))


def test_mix_use_force_propagate_and_propagate():

    analyzer = AstAnalyzer(os.path.join(TEST_PACKAGE_ROOT, 'mix_use_propagate_and_force_propagate_ACD-2845.py'))
    query = analyzer.query()

    # find all inner functions first
    query.function_nodes()
    while not query.is_end():
        query.function_nodes(force_propagate=False)

    module_usage = analyzer.get_module_usage('socket')
    query.propagate_nodes(ast_type=ast.Import, force_propagate=True)
    result = query.filter(Any(module_usage)).collect()
    assert len(result) == 3

    backup_query = query.persist()
    query.propagate_nodes(ast.Import, force_propagate=True)
    assert len(query.collect()) == 0
    assert query.is_end() == True

    query = backup_query
    query.propagate_nodes(ast.Import, force_propagate=False)
    assert len(query.collect()) == 3
    assert query.is_end() == True


def test_use_reset_to_reuse_query():

    analyzer = AstAnalyzer(os.path.join(TEST_PACKAGE_ROOT, 'call_nodes_propagate_ACD-2845.py'))
    query = analyzer.query()

    functions = query.function_nodes().collect()
    assert len(functions) == 2
    # query is stateful, so no call nodes will be returned
    functions = query.function_nodes().collect()
    assert len(functions) == 0

    query.reset()
    functions = query.function_nodes().collect()
    assert len(functions) == 2


def test_reset_feature():

    analyzer = AstAnalyzer(os.path.join(TEST_PACKAGE_ROOT, 'call_nodes_propagate_ACD-2845.py'))
    query = analyzer.query()
    while not query.is_end():
        query.propagate_nodes()
    query.reset()
    assert len(query._queue) == 1
    assert query._queue.popleft() == analyzer.root_ast_node
    assert query._parent_ast_node_dict == analyzer._parent_ast_node_dict


def test_use_persist_to_reuse_query():

    analyzer = AstAnalyzer(os.path.join(TEST_PACKAGE_ROOT, 'call_nodes_propagate_ACD-2845.py'))
    query = analyzer.query()

    functions = query.function_nodes().collect()
    assert len(functions) == 2
    # persist current state
    current_query = query.persist()

    functions = query.function_nodes().collect()
    assert len(functions) == 0

    # now current_query and query have different query state
    return_nodes = current_query.propagate_nodes(ast_type=ast.Return).collect()
    assert len(return_nodes) == 2


def test_persist_feature():

    analyzer = AstAnalyzer(os.path.join(TEST_PACKAGE_ROOT, 'call_nodes_propagate_ACD-2845.py'))
    query = analyzer.query().function_nodes()

    intermediate_query = query.persist()
    assert id(query) != id(intermediate_query)
    assert query._root_ast_node == intermediate_query._root_ast_node
    assert query._parent_ast_node_dict == intermediate_query._parent_ast_node_dict
    assert query._queue == intermediate_query._queue
    assert id(query._queue) != id(intermediate_query._queue)


def test_force_propagate_with_filter_function():

    analyzer = AstAnalyzer(os.path.join(TEST_PACKAGE_ROOT, 'call_nodes_propagate_ACD-2845.py'))
    query = analyzer.query()

    functions = query.function_nodes(filter_function=lambda node: node.name == 'func1').collect()
    assert len(functions) == 1
    assert functions[0].name == 'func1'


def test_complicated_force_propagate_with_filter_function_scenario():

    '''
        Try to return all nodes with lineno between 3 and 5
    '''
    analyzer = AstAnalyzer(os.path.join(TEST_PACKAGE_ROOT, 'call_nodes_propagate_ACD-2845.py'))
    query = analyzer.query()
    # propagate to line 3 first
    nodes = query.propagate_nodes(filter_function=
                    lambda node: hasattr(node, 'lineno') and node.lineno == 3).collect()

    while not query.is_end():
        next_batch_result = set(query.propagate_nodes(filter_function=
                                lambda node: hasattr(node, 'lineno') and node.lineno <= 5).collect())
        for node in next_batch_result:
            nodes.append(node)

    # func, return, attr, name
    assert len(nodes) == 4


def test_basic_any_filter_usage():

    if six.PY2:
        analyzer = AstAnalyzer(os.path.join(TEST_PACKAGE_ROOT, 'basic_any_and_all_filter_usage_ACD-2845_py2.py'))
    else:
        analyzer = AstAnalyzer(os.path.join(TEST_PACKAGE_ROOT, 'basic_any_and_all_filter_usage_ACD-2845_py3.py'))
    query = analyzer.query()

    nodes = query.function_nodes().filter(Any(analyzer.get_module_usage('socket.SOCK_DGRAM'))).collect()
    assert len(nodes) == 2
    assert set(map(lambda node: node.name, nodes)) == {'func1', 'func3'}

    query.reset()
    nodes = query.function_nodes().filter(Any(analyzer.get_module_usage('socket.AF_INET6'))).collect()
    assert len(nodes) == 1
    assert nodes[0].name == 'func2'


def test_basic_or_filter_usage():

    if six.PY2:
        analyzer = AstAnalyzer(os.path.join(TEST_PACKAGE_ROOT, 'basic_any_and_all_filter_usage_ACD-2845_py2.py'))
    else:
        analyzer = AstAnalyzer(os.path.join(TEST_PACKAGE_ROOT, 'basic_any_and_all_filter_usage_ACD-2845_py3.py'))
    query = analyzer.query()

    nodes = query.function_nodes().filter(All(analyzer.get_module_usage('socket.AF_INET'))).collect()
    assert len(nodes) == 0

    query.reset()
    nodes = query.function_nodes().filter(All(analyzer.get_module_usage('socket.AF_INET6'))).collect()
    assert len(nodes) == 1
    assert nodes[0].name == 'func2'


def test_basic_and_and_or_filter_usage():

    analyzer = AstAnalyzer(os.path.join(TEST_PACKAGE_ROOT, 'basic_and_and_or_filter_usage_ACD-2845.py'))
    query = analyzer.query()

    nodes = query.call_nodes().filter(
                And(Any(analyzer.get_module_usage('socket.AF_INET')),
                    Any(analyzer.get_module_usage('socket.SOCK_STREAM')))).collect()
    assert len(nodes) == 1
    assert nodes[0].lineno == 7

    query.reset()
    nodes = query.call_nodes().filter(
                And(Any(analyzer.get_module_usage('socket.AF_INET6')),
                    Any(analyzer.get_module_usage('socket.SOCK_STREAM')))).collect()
    assert len(nodes) == 0

    # Collect all call nodes with module `socket.AF_INET` or `socket.SOCK_DGRAM` usages
    query.reset()
    nodes = query.call_nodes().filter(
                Or(Any(analyzer.get_module_usage('socket.AF_INET')),
                   Any(analyzer.get_module_usage('socket.SOCK_DGRAM')))).collect()
    assert len(nodes) == 3

    # Collect all attribute usages with module `socket.AF_INET` and `socket.SOCK_DGRAM`
    query.reset()
    nodes = query.attribute_nodes().filter(
                Or(Any(analyzer.get_module_usage('socket.AF_INET')),
                   Any(analyzer.get_module_usage('socket.SOCK_DGRAM')))).collect()
    assert len(nodes) == 4


def test_basic_multi_and_and_multi_or_usage():

    analyzer = AstAnalyzer(os.path.join(TEST_PACKAGE_ROOT, 'basic_multi_and_and_or_filter_usage_ACD-2845.py'))
    query = analyzer.query()

    nodes = query.call_nodes().filter(
                MultiAnd(Any(analyzer.get_module_function_call_usage('socket', 'socket')),
                         Any(analyzer.get_module_usage('socket.AF_INET')),
                         Any(analyzer.get_module_usage('socket.SOCK_DGRAM')))).collect()
    assert len(nodes) == 1
    assert nodes[0].lineno == 3

    query.reset()
    nodes = query.call_nodes().filter(
                MultiAnd(Any(analyzer.get_module_function_call_usage('socket', 'socket')),
                         Any(analyzer.get_module_usage('socket.SOCK_STREAM')))).collect()
    assert len(nodes) == 2
    nodes.sort(key = lambda node: node.lineno)
    assert (nodes[0].lineno , nodes[1].lineno) == (5 , 7)

    query.reset()
    nodes = query.call_nodes().filter(
                MultiOr(Any(analyzer.get_module_usage('socket.SOCK_DGRAM')),
                        Any(analyzer.get_module_usage('socket.AF_INET6')))).collect()
    assert len(nodes) == 2
    nodes.sort(key = lambda node: node.lineno)
    assert (nodes[0].lineno, nodes[1].lineno) == (3 , 5)

    query.reset()
    nodes = query.call_nodes().filter(
                MultiOr(Any(analyzer.get_module_usage('socket.AF_INET6')),
                        Any(analyzer.get_module_usage('socket.SOCK_DGRAM')),
                        Any(analyzer.get_module_usage('socket.AF_INET')))).collect()
    assert len(nodes) == 3
    nodes.sort(key=lambda node: node.lineno)
    assert list(map(lambda node: node.lineno, nodes)) == [3, 5, 7]


def test_advanced_and_and_or_combination():

    analyzer = AstAnalyzer(os.path.join(TEST_PACKAGE_ROOT, 'advanced_and_and_or_combination_ACD-2845.py'))
    query = analyzer.query()

    usernames = analyzer.get_variable_distribution('username')
    passwords = analyzer.get_variable_distribution('password')

    # find all functions contain username or password usages
    query.function_nodes()
    all_nodes = []
    while not query.is_end():
        nodes = query.filter(Or(Any(usernames), Any(passwords))).collect()
        all_nodes.extend(nodes)
        query.function_nodes()
    assert len(all_nodes) == 4
    all_nodes.sort(key = lambda node: node.name)
    assert (all_nodes[0].name, all_nodes[1].name, all_nodes[2].name, all_nodes[3].name) == \
           ('func', 'func1', 'func2', 'func3')

    # find all functions contain all username and all password usage
    query.reset()
    query.function_nodes()
    all_nodes = []
    while not query.is_end():
        nodes = query.filter(And(All(usernames), All(passwords))).collect()
        all_nodes.extend(nodes)
        query.function_nodes()
    assert len(all_nodes) == 1
    assert all_nodes[0].name == 'func'


def test_if_root_node_could_be_filtered():

    analyzer = AstAnalyzer(os.path.join(TEST_PACKAGE_ROOT, 'simple_function_call_ACD-2845.py'))
    nodes = analyzer.query().call_nodes() \
                    .filter(Any(analyzer.get_module_function_call_usage('socket', 'socket'))) \
                    .filter(Any(analyzer.get_module_usage('socket.AF_INET'))) \
                    .filter(Any(analyzer.get_module_usage('socket.SOCK_DGRAM'))).collect()
    assert len(nodes) == 1
    assert nodes[0].lineno == 3


def test_if_different_approaches_return_same_result():

    if six.PY2:
        analyzer = AstAnalyzer(os.path.join(TEST_PACKAGE_ROOT, 'basic_any_and_all_filter_usage_ACD-2845_py2.py'))
    else:
        analyzer = AstAnalyzer(os.path.join(TEST_PACKAGE_ROOT, 'basic_any_and_all_filter_usage_ACD-2845_py3.py'))

    function_call_nodes = analyzer.get_module_function_call_usage('socket', 'socket')
    nodes1 = analyzer.get_module_usage('socket.AF_INET')
    nodes2 = analyzer.get_module_usage('socket.SOCK_DGRAM')

    query = analyzer.query()
    while not query.is_end():
        query.call_nodes(force_propagate=False)
    # approach one, filter chain
    sub_query = query.persist()
    result = sub_query.filter(Any(function_call_nodes)).filter(Any(nodes1)).filter(Any(nodes2)).collect()
    assert len(result) == 1
    assert result[0].lineno == 4
    # approach two, use binary and
    sub_query = query.persist()
    result = sub_query.filter(And(And(Any(function_call_nodes), Any(nodes1)),
                                  Any(nodes2))).collect()
    assert len(result) == 1
    assert result[0].lineno == 4
    # approach three, use MultiAnd
    sub_query = query.persist()
    result = sub_query.filter(MultiAnd(Any(function_call_nodes), Any(nodes1), Any(nodes2))).collect()
    assert len(result) == 1
    assert result[0].lineno == 4


def test_very_complicated_scenario():

    # find all call nodes which username and password usages are included in call_node's subtree
    # and call_nodes should be nested in a function call
    #
    #
    #                     call_nodes   any username or password
    #                  /
    #   function nodes
    #                  \
    #                     print_nodes  any username or password
    #
    #
    if six.PY2:
        analyzer = AstAnalyzer(os.path.join(TEST_PACKAGE_ROOT, 'very_complicated_scenario_ACD-2845_py2.py'))
    else:
        analyzer = AstAnalyzer(os.path.join(TEST_PACKAGE_ROOT, 'very_complicated_scenario_ACD-2845_py3.py'))

    usernames = analyzer.get_variable_distribution('username')
    passwords = analyzer.get_variable_distribution('password')

    result_set = set()

    # push to function layer first
    query = analyzer.query().function_nodes(force_propagate=True)
    sub_query = query.persist()
    # find inner call nodes, try force propagate first
    sub_query.propagate_nodes(ast_type=ast.Call, force_propagate=True)
    while not sub_query.is_end():
        sub_query.propagate_nodes(ast_type=ast.Call, force_propagate=False)
    nodes = sub_query.filter(Or(Any(usernames), Any(passwords))).collect()
    result_set |= set(nodes)
    # find inner print nodes, try force propagate first
    # here we use ast.Print node, so it will work in python2 only
    if six.PY2:
        sub_query = query.persist()
        sub_query.propagate_nodes(ast_type=ast.Print, force_propagate=True)
        while not sub_query.is_end():
            sub_query.propagate_nodes(ast_type=ast.Print, force_propagate=False)
        nodes = sub_query.filter(Or(Any(usernames), Any(passwords))).collect()
        result_set |= set(nodes)

        result_list = list(result_set)
        result_list.sort(key = lambda node: node.lineno)
        assert map(lambda node: node.lineno, result_list) == [9, 13, 17, 24, 29, 30]
        assert len(filter(lambda node: isinstance(node, ast.Call), result_list)) == 3
        assert len(filter(lambda node: isinstance(node, ast.Print), result_list)) == 3
        # we find the inner call node exactly
        assert result_list[4].func.id == 'hehe'