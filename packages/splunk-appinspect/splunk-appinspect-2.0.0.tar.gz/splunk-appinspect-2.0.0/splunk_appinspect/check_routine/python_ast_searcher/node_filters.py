import ast


def is_sub_class_def(node, ast_info):
    parent_node = ast_info.get_parent_ast_node(node)
    return isinstance(parent_node, ast.ClassDef)
