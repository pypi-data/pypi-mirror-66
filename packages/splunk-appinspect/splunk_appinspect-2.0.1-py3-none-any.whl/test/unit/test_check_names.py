import os
import ast
import splunk_appinspect

DEFAULT_CHECKS_DIR = splunk_appinspect.checks.DEFAULT_CHECKS_DIR


def test_check_names_are_unique():
    """check if all check names are global unique"""
    check_name_to_filepath = {}
    for filepath in filter(lambda filepath: filepath.endswith('.py') and
                           filepath.startswith('check_'), os.listdir(DEFAULT_CHECKS_DIR)):
        check_filepath = os.path.join(DEFAULT_CHECKS_DIR, filepath)
        with open(check_filepath, 'r') as f:
            ast_root = ast.parse(f.read())
            # check first layer function
            for node in filter(lambda node:
                               isinstance(node, ast.FunctionDef) and
                               node.name.startswith('check_'), ast_root.body):
                assert node.name not in check_name_to_filepath, \
                    'Check `{}` both exists in `{}` and `{}`'.format(node.name, check_name_to_filepath[node.name], filepath)
                check_name_to_filepath[node.name] = filepath