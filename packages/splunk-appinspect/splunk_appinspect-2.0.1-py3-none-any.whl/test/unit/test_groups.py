"""This is a test module geared towards testing the Group class of Splunk
AppInspect.
"""
# Copyright 2016 Splunk Inc. All rights reserved.

# Python Standard Libraries
import imp
import os
import re
# Third-Party Library
import bs4
# Custom Libraries
import splunk_appinspect


CURRENT_DIRECTORY = os.path.dirname(os.path.abspath(__file__))
CHECKS_DIRECTORY = os.path.abspath(os.path.join(CURRENT_DIRECTORY, "..", "..", "splunk_appinspect", "checks"))


def test_get_doc():
    """Test ability to retrieve doc-string documentation from the Group object's
    method.
    """
    test_name = "test.module.name"
    test_module = imp.new_module(test_name)

    test_group = splunk_appinspect.checks.Group(test_module)
    assert test_group.doc() == test_name, "Group.doc() is incorrect."

    test_module.__doc__ = "Fuggle"
    assert test_group.doc() == "Fuggle", "Group.doc() is incorrect."


def test_doc_name_human_readable():
    """Test ability to retrieve doc-string documentation heading from the Group
    object's doc_name_human_readable method.
    """
    test_name = "test.module.name"
    test_module = imp.new_module(test_name)

    test_group = splunk_appinspect.checks.Group(test_module)
    assert test_group.doc() == test_name, "Group.doc() is incorrect."

    test_module.__doc__ = """
### Fuggle Title

Fuggles are very important.
    """
    assertion_output = "Group.doc_name_human_readable() is incorrect."
    assert test_group.doc_name_human_readable() == "Fuggle Title", assertion_output


def test_get_doc_html():
    """Test ability to retrieve html formatted doc-string documentation from the
    Group object's doc_html() method for all groups and that the HTML has the
    expected formatting of the form:
    <h3><a name="my_group_name_based_on_python_file"></a>My Desc in English</h3>
    <p>My docstring for this group.</p>
    """
    appinspect_groups = splunk_appinspect.checks.groups()
    for group in appinspect_groups:
        html = group.doc_html()
        type_message = "group.doc_html() was not of type unicode."
        from builtins import str as text
        assert type(html) == text, type_message
        # Use BeautifulSoup to analyze the structure of the HTML
        bs_html = bs4.BeautifulSoup(html, 'html.parser')
        contents_message = (u"group.doc_html() was not of the expected form."
                            u" Found: \n{}\n\n Expected: \n"
                            u" <h3><a name='my_group_name_from_python_file'>"
                            u" </a>Markdown Heading from group docstring</h3>"
                            u" <!-- Zero or more paragraphs of the form: -->"
                            u" <p>Markdown Paragraph from group docstring</p>"
                            .format(html))
        found_h3 = False
        found_a = False
        for elem in bs_html.contents:
            if isinstance(elem, bs4.element.Tag):
                if elem.name == "h3":
                    # If multiple <h3> elements, this is unexpected
                    assert not found_h3, contents_message
                    found_h3 = True
                    # Look through the subelem of <h3>, <a> should be here
                    for subelem in elem.contents:
                        if isinstance(subelem, bs4.element.Tag):
                            if subelem.name == "a":
                                # If multiple <a> elements, this is unexpected
                                assert not found_a, contents_message
                                found_a = True
        assert found_h3, contents_message
        assert found_a, contents_message


def test_tags_returns_correct_tags():
    """Test that all the tags that exist in check module are correctly returned
    from the Group object context.
    """
    tag_regex_patterns = "@splunk_appinspect.tags\((.*)\)"
    compiled_tag_regex_pattern = re.compile(tag_regex_patterns,
                                            re.IGNORECASE and re.MULTILINE)
    appinspect_groups = splunk_appinspect.checks.groups()

    # Ignores disabled check files and compiled python files
    file_names = [
        file_name
        for file_name in os.listdir(CHECKS_DIRECTORY)
        if (os.path.isfile(os.path.join(CHECKS_DIRECTORY, file_name)) and
            file_name.endswith(".py") and
            not file_name.startswith("disabled"))
    ]

    # Iterate through each of the files
    # extract the tags
    # find all tags in the file
    # compare against the group object's tags
    for full_file_name in file_names:
        file_name, file_extension = os.path.splitext(full_file_name)
        file_path = os.path.join(CHECKS_DIRECTORY, full_file_name)

        matching_groups = [
            group
            for group in appinspect_groups
            if group.name == file_name
        ]

        assert_error = (("Multiple-groups with the same name have been detected."
                         "The group: {}, has been detected more than once.")
                        .format(full_file_name))
        assert len(matching_groups) == 1, assert_error

        current_group = matching_groups[0]

        with open(file_path, "r") as file:
            raw_file_contents = file.read()

        tag_matches = compiled_tag_regex_pattern.findall(raw_file_contents)

        raw_file_tags = tag_matches

        parsed_raw_file_tags = ",".join(raw_file_tags)
        parsed_raw_file_tags = parsed_raw_file_tags.replace("\"", "")
        parsed_raw_file_tags = parsed_raw_file_tags.replace("\'", "")
        parsed_raw_file_tags = parsed_raw_file_tags.replace(" ", "")
        parsed_raw_file_tags = parsed_raw_file_tags.strip()
        parsed_raw_file_tags = parsed_raw_file_tags.split(",")

        current_group_tags = set(current_group.tags())

        unique_tag_matches = set(parsed_raw_file_tags)

        do_all_tags_in_the_file_exist_in_group_objects_tags = set(unique_tag_matches).issubset(current_group_tags)

        assert do_all_tags_in_the_file_exist_in_group_objects_tags


def test_group_check_retrieval_values():
    """Test ability to assign and retrieve checks in the group."""

    def check_function():
        return "sure."

    def not_to_be_returned():
        raise Exception("This should not be called")

    test_group_name = "test.module.name"

    test_module = imp.new_module(test_group_name)
    test_module.check_function = check_function
    test_module.not_to_be_returned = not_to_be_returned

    test_checks = splunk_appinspect.checks.generate_checks(test_module)

    test_group_auto_populate = splunk_appinspect.checks.Group(test_module)
    test_group_manually_populated = splunk_appinspect.checks.Group(test_module, test_checks)

    assert len(list(test_group_auto_populate.checks())) == 1, "Should have one check."
    for check in test_group_auto_populate.checks():
        assert check.name == "check_function", "Incorrect check function returned."

    assert len(list(test_group_manually_populated.checks())) == 1, "Should have one check."
    for check in test_group_manually_populated.checks():
        assert check.name == "check_function", "Incorrect check function returned."


def test_all_checks_should_be_returned_when_tagging_not_used():
    test_group_name = "test.module.name"
    test_module = imp.new_module(test_group_name)

    def check_test_one():
        pass

    def check_test_two():
        pass

    def check_test_three():
        pass

    test_module.check_test_one = check_test_one
    test_module.check_test_two = check_test_two
    test_module.check_test_three = check_test_three

    test_group = splunk_appinspect.checks.Group(test_module)

    check_list = [check
                  for check in test_group.checks()]

    assert len(check_list) == 3, "Should have three checks"


def test_all_checks_should_be_returned_when_no_filter_specified():
    test_group_name = "test.module.name"
    test_module = imp.new_module(test_group_name)

    @splunk_appinspect.tags("a", "c")
    def check_test_one():
        pass

    @splunk_appinspect.tags("a", "b")
    def check_test_two():
        pass

    @splunk_appinspect.tags("d")
    def check_test_three():
        pass

    test_module.check_test_one = check_test_one
    test_module.check_test_two = check_test_two
    test_module.check_test_three = check_test_three

    test_group = splunk_appinspect.checks.Group(test_module)

    check_list = [check
                  for check in test_group.checks()]

    assert len(check_list) == 3, "Should have three checks"


################################################################################
# Group Retrieval of Tagged Checks Goes Here
################################################################################
def test_only_included_tagged_check_should_be_returned():
    """Test the splunk_appinspect.checks.generate_group command successful
    filtering of included tagged checks.
    """
    test_group_name = "test.module.name"
    test_module = imp.new_module(test_group_name)

    @splunk_appinspect.tags("a", "c")
    def check_test_one():
        pass

    @splunk_appinspect.tags("a", "b")
    def check_test_two():
        pass

    @splunk_appinspect.tags("d")
    def check_test_three():
        pass

    test_module.check_test_one = check_test_one
    test_module.check_test_two = check_test_two
    test_module.check_test_three = check_test_three

    included_group_a_tag = splunk_appinspect.checks.generate_group(test_module,
                                                                   included_tags=["a"])
    included_b_d_tag = splunk_appinspect.checks.generate_group(test_module,
                                                               included_tags=["b", "d"])
    included_a_c_d_tag = splunk_appinspect.checks.generate_group(test_module,
                                                                 included_tags=["a", "c", "d"])
    included_a_b_c_d_tag = splunk_appinspect.checks.generate_group(test_module,
                                                                   included_tags=["a", "b", "c", "d"])

    check_list = list(included_group_a_tag.checks())
    check_bool_list = [check.has_tag(["a"])
                       for check in check_list]
    assert len(check_list) == 2, "Should have found two checks."
    assert False not in check_bool_list, "Check tag not found."

    check_list = list(included_b_d_tag.checks())
    check_bool_list = [check.has_tag(["b", "d"])
                       for check in check_list]
    assert len(check_list) == 2, "Should have found two checks."
    assert False not in check_bool_list, "Check tag not found."

    check_list = list(included_a_c_d_tag.checks())
    check_bool_list = [check.has_tag(["a", "c", "d"])
                       for check in check_list]
    assert len(check_list) == 3, "Should have found three checks."
    assert False not in check_bool_list, "Check tag not found."

    check_list = list(included_a_b_c_d_tag.checks())
    check_bool_list = [check.has_tag(["a", "b", "c", "d"])
                       for check in check_list]
    assert len(check_list) == 3, "Should have found three checks."
    assert False not in check_bool_list, "Check tag not found."


def test_excluded_tagged_check_should_not_be_returned():
    """Test the splunk_appinspect.checks.generate_group command successful
    filtering of excluded checks.
    """
    test_group_name = "test.module.name"
    test_module = imp.new_module(test_group_name)

    @splunk_appinspect.tags("a", "c")
    def check_test_one():
        pass

    @splunk_appinspect.tags("a", "b")
    def check_test_two():
        pass

    @splunk_appinspect.tags("d")
    def check_test_three():
        pass

    test_module.check_test_one = check_test_one
    test_module.check_test_two = check_test_two
    test_module.check_test_three = check_test_three

    excluded_group_a_tag = splunk_appinspect.checks.generate_group(test_module,
                                                                   excluded_tags=["a"])
    excluded_b_d_tag = splunk_appinspect.checks.generate_group(test_module,
                                                               excluded_tags=["b", "d"])
    excluded_a_c_d_tag = splunk_appinspect.checks.generate_group(test_module,
                                                                 excluded_tags=["a", "c", "d"])
    excluded_a_b_c_d_tag = splunk_appinspect.checks.generate_group(test_module,
                                                                   excluded_tags=["a", "b", "c", "d"])

    check_list = list(excluded_group_a_tag.checks())
    check_bool_list = [check.has_tag(["a"])
                       for check in check_list]
    assert len(check_list) == 1, "Should have found one check."
    assert True not in check_bool_list, "Check tag should not have been found."

    check_list = list(excluded_b_d_tag.checks())
    check_bool_list = [check.has_tag(["b", "d"])
                       for check in check_list]
    assert len(check_list) == 1, "Should have found one check."
    assert True not in check_bool_list, "Check tag should not have been found."

    check_list = list(excluded_a_c_d_tag.checks())
    check_bool_list = [check.has_tag(["a", "c", "d"])
                       for check in check_list]
    assert len(check_list) == 0, "Should have found no checks."
    assert True not in check_bool_list, "Checks should not have been found."

    check_list = list(excluded_a_b_c_d_tag.checks())
    check_bool_list = [check.has_tag(["a", "b", "c", "d"])
                       for check in check_list]
    assert len(check_list) == 0, "Should have found one checks."
    assert True not in check_bool_list, "Checks should not have been found."


def test_check_include_and_exclude_tag_filtering():
    """Test the splunk_appinspect.checks.generate_group command successful
    filtering of both included and excluded checks.
    """

    test_group_name = "test.module.name"
    test_module = imp.new_module(test_group_name)

    @splunk_appinspect.tags("a", "c")
    def check_test_one():
        pass

    @splunk_appinspect.tags("a", "b")
    def check_test_two():
        pass

    @splunk_appinspect.tags("d")
    def check_test_three():
        pass

    test_module.check_test_one = check_test_one
    test_module.check_test_two = check_test_two
    test_module.check_test_three = check_test_three

    mixed_group_include_a_exclude_a_tag = splunk_appinspect.checks.generate_group(test_module,
                                                                                  included_tags=["a"],
                                                                                  excluded_tags=["a"])
    mixed_include_a_exclude_d_tag = splunk_appinspect.checks.generate_group(test_module,
                                                                            included_tags=["a"],
                                                                            excluded_tags=["d"])
    mixed_include_a_d_exclude_d_tag = splunk_appinspect.checks.generate_group(test_module,
                                                                              included_tags=["a", "d"],
                                                                              excluded_tags=["d"])
    mixed_include_c_d_exclude_b_tag = splunk_appinspect.checks.generate_group(test_module,
                                                                              included_tags=["c", "d"],
                                                                              excluded_tags=["b"])

    # Included tag should take precedence
    check_list = list(mixed_group_include_a_exclude_a_tag.checks())
    check_bool_list = [check.has_tag(["a"])
                       for check in check_list]
    assert len(check_list) == 2, "Should have found two checks."
    assert False not in check_bool_list, "Check not found."

    check_list = list(mixed_include_a_exclude_d_tag.checks())
    check_included_bool_list = [check.has_tag(["a"])
                                for check in check_list]
    check_excluded_bool_list = [check.has_tag(["d"])
                                for check in check_list]
    assert len(check_list) == 2, "Should have found two checks."
    assert False not in check_included_bool_list, "Check not found."
    assert True not in check_excluded_bool_list, "Check tag should not have been found."

    # Included tag should take precedence
    check_list = list(mixed_include_a_d_exclude_d_tag.checks())
    check_included_bool_list = [check.has_tag(["a", "d"])
                                for check in check_list]
    assert len(check_list) == 3, "Should have found three checks."
    assert False not in check_included_bool_list, "Check not found."

    # Included tag should take precedence
    check_list = list(mixed_include_c_d_exclude_b_tag.checks())
    check_included_bool_list = [check.has_tag(["c", "d"])
                                for check in check_list]
    check_excluded_bool_list = [check.has_tag(["b"])
                                for check in check_list]
    assert len(check_list) == 2, "Should have found two checks."
    assert False not in check_included_bool_list, "Check not found."
    assert True not in check_excluded_bool_list, "Check tag should not have been found."
