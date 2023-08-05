#!/usr/bin/env python

from __future__ import print_function
import ast
import os
import splunk_appinspect

DEFAULT_CHECKS_DIR = splunk_appinspect.checks.DEFAULT_CHECKS_DIR


def get_check_files(path):
    return filter(lambda x: x.endswith('.py'), os.listdir(path))


def get_checks_and_helpers(module):
    checks = []
    helpers = {}
    for node in module.body:
        if type(node) == ast.FunctionDef:
            if node.name.startswith('check'):
                checks.append(node)
            else:
                helpers[node.name] = [node]

    return checks, helpers


def get_actions_and_tags(function, helpers):
    actions = []
    tags = None
    reporter_id = 'reporter'
    for node in ast.walk(function):
        if type(node) == ast.Call and type(node.func) == ast.Attribute:
            if type(node.func.value) == ast.Name:
                func = node.func
                if reporter_id == func.value.id:
                    actions.append(func.attr)
                if func.value.id == 'splunk_appinspect' and func.attr == 'tags':
                    tags = [arg.s for arg in node.args]

        elif type(node) == ast.Call and type(node.func) == ast.Name:
            name = node.func.id
            if name in helpers and name != function.name:
                helper = helpers[name]
                if len(helper) == 1:
                    sub_actions, _ = get_actions_and_tags(helper[0], helpers)
                    helper.append(sub_actions)
                sub_actions = helper[1]
                actions = list(set(actions) | set(sub_actions))

    return actions, tags


def check_function_tag(filename):
    results = []
    path = os.path.join(DEFAULT_CHECKS_DIR, filename)
    fd = open(path, 'r')
    module = ast.parse(fd.read())

    checks, helpers = get_checks_and_helpers(module)

    for check in checks:
        actions, tags = get_actions_and_tags(check, helpers)
        assert not (('manual_check' in actions or 'ast_manual_check' in actions) ^ ('manual' in tags)), \
            'Please verify tag `manual` of check `{}` in {}'.format(check.name, filename)
        results.append((tags, check.name, filename))

    return results


def test_tag_usage():
    print("-" * 10 + "running tag validation check" + "-" * 10)
    check_files = get_check_files(DEFAULT_CHECKS_DIR)
    all_tags = []
    for filename in check_files:
        all_tags.extend(check_function_tag(filename))

    print("{} cloud checks".format(len(list(filter(lambda tags: 'cloud' in tags[0], all_tags)))))
    print("{} manual checks".format(len(list(filter(lambda tags: 'manual' in tags[0], all_tags)))))
    print("{} checks with tags 'cloud' and 'manual'".format(
        len(list(filter(lambda tags: 'manual' in tags[0] and 'cloud' in tags[0], all_tags)))))
    print("-" * 48)
