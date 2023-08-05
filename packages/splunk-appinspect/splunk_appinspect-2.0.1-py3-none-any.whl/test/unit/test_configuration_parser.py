# Copyright 2016 Splunk Inc. All rights reserved.

# Python Standard Libraries
from __future__ import print_function
# Third-Party Libraries
import pytest
# Custom Libraries
import splunk_appinspect.configuration_file
import splunk_appinspect.configuration_parser


def test_join_lines():
    text = """ this is a\\
test
which should come to two items """
    result = [line
              for line
              in splunk_appinspect.configuration_parser.join_lines(text.split('\n'))]
    assert result == [(" this is a\ntest", 2, None),
                      ("which should come to two items ", 3, None)]


def test_returns_error_on_whitespace_with_continuation():
    """ This is a circumstance in which the Splunk splunk_appinspect.configuration_parser just does the wrong
    thing. We want to raise when we see it, because it's going to be an issue."""
    text = """baz \\\t
    baf """
    print(text)
    results = [line[2]
               for line
               in splunk_appinspect.configuration_parser.join_lines(text.split('\n'))]
    assert 'trailing whitespace' in results[0]


def test_get_whitespace():
    results = [row
               for row
               in splunk_appinspect.configuration_parser.configuration_lexer(['', ' ', '\t', '\n'])]
    assert results == [('WHITESPACE', '', 1, None), ('WHITESPACE', '', 2, None),
                       ('WHITESPACE', '', 3, None), ('WHITESPACE', '', 4, None)]


def test_get_comments():
    tests = ['; foo', '# foo', '  # comment', '; [basil]']
    expected = ['; foo', '# foo', '# comment', '; [basil]']
    results = [row[1]
               for row
               in splunk_appinspect.configuration_parser.configuration_lexer(tests)
               if row[0] == 'COMMENT']
    assert results == expected


def test_get_stanza_from_conf_file():
    tests = ['[foo]', '  [bar]', '[baz]lsjslj', '[  basil]', '[foo\\', 'bar]', '[[-0-9a-z]*.log]']
    expected = ['foo', 'bar', 'baz', '  basil', 'foo\nbar', '[-0-9a-z]*.log']
    results = [row[1]
               for row
               in splunk_appinspect.configuration_parser.configuration_lexer(tests)
               if row[0] == 'STANZA']
    assert results == expected

def test_get_stanza_from_spec_file():
    tests = ['[foo]', '  [bar]', '[baz]lsjslj', '[  basil]', '[foo\\', 'bar]', '[[-0-9a-z]*.log]']
    expected = ['foo', 'baz', '  basil', 'foo\nbar', '[-0-9a-z]*.log']
    results = [row[1]
               for row
               in splunk_appinspect.configuration_parser.specification_lexer(tests)
               if row[0] == 'STANZA']
    assert results == expected


def test_get_key_value():
    tests = ['foo=bar', '  bif=bang', 'bork=chef  ', 'baz foo = bar', 'zig =zag jig']
    expected = [('foo', 'bar'), ('bif', 'bang'), ('bork', 'chef'), ('zig', 'zag jig')]
    results = [row[1]
               for row
               in splunk_appinspect.configuration_parser.configuration_lexer(tests)
               if row[0] == 'KEYVAL']
    assert results == expected

def test_get_stanza_lineno():
    test_conf_str = """
      [foo]
      default=1
      # don't mind me
      [bar]
      t=0
      r=True
      key=val

      # comment
      [bang]
      #comment

      [bork]

      """
    tests = test_conf_str.split('\n')
    expected = [('foo', 2),
                ('bar', 5),
                ('bang', 11),
                ('bork', 14)]
    results = [(row[1], row[2])
               for row
               in splunk_appinspect.configuration_parser.configuration_lexer(tests)
               if row[0] == 'STANZA']
    assert results == expected

def test_get_key_value_lineno():
    test_conf_str = """
      [foo]
      default=1
      # don't mind me
      [bar]
      t=0
      r=True
      key=val

      """
    tests = test_conf_str.split('\n')
    expected = [('default', '1', 3),
                ('t', '0', 6),
                ('r', 'True', 7),
                ('key', 'val', 8)]
    results = [(row[1][0], row[1][1], row[2])
               for row
               in splunk_appinspect.configuration_parser.configuration_lexer(tests)
               if row[0] == 'KEYVAL']
    assert results == expected

def test_continuation_in_comment():
    # The following line will be discarded, so it shouldn't throw an error
    conf = """
    foo \\\t
    bar
    """
    file = splunk_appinspect.configuration_parser.parse(
        conf, splunk_appinspect.configuration_file.ConfigurationFile(), splunk_appinspect.configuration_parser.configuration_lexer)
    assert len(file.errors) == 0


def test_continuation_in_kv():
    # The following line contains a key-value- trailing whitespace should be
    # an error
    conf = """
    baz=foo \\\t
    bar
    """
    file = splunk_appinspect.configuration_parser.parse(
        conf, splunk_appinspect.configuration_file.ConfigurationFile(), splunk_appinspect.configuration_parser.configuration_lexer)
    print(file.errors)
    assert 'trailing whitespace' in file.errors[0][0]
    assert len(file.errors) == 1


def test_string_parse():
    conf = """
[default]
foo.boo = bar

[wombat]
fang=heart
    """
    configuration_file = splunk_appinspect.configuration_file.ConfigurationFile()
    configuration_file = splunk_appinspect.configuration_parser.parse(conf,
                                                                      configuration_file,
                                                                      splunk_appinspect.configuration_parser.configuration_lexer)
    assert configuration_file.has_section('wombat') == True
    assert configuration_file.has_section('badger') == False
    assert configuration_file.get('wombat', 'fang') == 'heart'
    assert list(configuration_file.section_names()) == ['default', 'wombat']
    assert configuration_file.items('default') == [('foo.boo', 'bar', 3)]
    with pytest.raises(splunk_appinspect.configuration_file.NoOptionError) as excinfo:
        configuration_file.get('wombat', 'nonexistent')
    with pytest.raises(splunk_appinspect.configuration_file.NoSectionError) as excinfo:
        configuration_file.get('not_here', 'nonexistent')
    assert configuration_file.has_option('wombat', 'fang') == True
    assert configuration_file.has_option('missing', 'gone') == False


# For testing the iterator logic of the conf file
# I tried to keep this like our test scenarios, but there's a lot of setup
# required for that. Instead I just generate the path and expected output, then
# test against that.

# TODO: find new conf files to parse (these moved to other project)
# invalid_conf_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)),
#                                       "packages",
#                                       "has_savedsearches_conf_with_multiline_search_that_has_trailing_whitespace_at_end",
#                                       "default",
#                                       "savedsearches.conf")
# valid_conf_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)),
#                                     "packages",
#                                     "has_valid_savedsearches_conf_with_multiline_search",
#                                     "default",
#                                     "savedsearches.conf")
# conf_files = [(invalid_conf_file_path, "failure"),
#               (valid_conf_file_path, "success")]


# @pytest.mark.parametrize("conf_file_path, expected_result", conf_files)
# def test_conf_iterator_parse(conf_file_path, expected_result):
#     try:
#         file_handle = open(conf_file_path)
#         configuration_file = splunk_appinspect.configuration_file.ConfigurationFile()
#         configuration_file = splunk_appinspect.configuration_parser.parse(file_handle,
#                                                                 configuration_file,
#                                                                 splunk_appinspect.configuration_parser.configuration_lexer)
#     except:
#         assert expected_result == "failure"
