# Copyright 2017 Splunk Inc. All rights reserved.

# Python Standard Libraries
# Third-Party Library
import pytest

# Custom Libraries
from splunk_appinspect.reporter import Reporter


def test_reporter_fail():
    """Test formatting of reporter using failure and files.
    """
    message = "Hello"
    reporter = Reporter()
    reporter.fail(message)
    assert reporter.state() == "failure"
    assert message == reporter.report_records()[0].message
    reporter = Reporter()
    reporter.assert_fail(False, message)
    assert reporter.state() == "failure"
    assert message == reporter.report_records()[0].message


def test_reporter_fail_with_file():
    """Test formatting of reporter using failure and files.
    """
    message = "Hello"
    filename = "a.txt"
    reporter = Reporter()
    reporter.fail(message, file_name=filename)
    assert reporter.state() == "failure"
    assert filename in reporter.report_records()[0].message


def test_reporter_fail_with_file_and_line():
    """Test formatting of reporter using failure, files and line.
    """
    message = "Hello"
    filename = "a.txt"
    line_number = 1
    reporter = Reporter()
    reporter.fail(message, file_name=filename, line_number=line_number)
    assert reporter.state() == "failure"
    assert filename in reporter.report_records()[0].message
    assert str(line_number) in reporter.report_records()[0].message


def test_reporter_warn():
    """Test formatting of reporter using warn and files.
    """
    message = "Hello"
    reporter = Reporter()
    reporter.warn(message)
    assert reporter.state() == "warning"
    assert message == reporter.report_records()[0].message
    reporter = Reporter()
    reporter.assert_warn(False, message)
    assert reporter.state() == "warning"
    assert message == reporter.report_records()[0].message


def test_reporter_warn_with_file():
    """Test formatting of reporter using warn and files.
    """
    message = "Hello"
    filename = "a.txt"
    reporter = Reporter()
    reporter.warn(message, file_name=filename)
    assert reporter.state() == "warning"
    assert filename in reporter.report_records()[0].message


def test_reporter_warn_with_file_and_line():
    """Test formatting of reporter using warn, files and line.
    """
    message = "Hello"
    filename = "a.txt"
    line_number = 1
    reporter = Reporter()
    reporter.warn(message, file_name=filename, line_number=line_number)
    assert reporter.state() == "warning"
    assert filename in reporter.report_records()[0].message
    assert str(line_number) in reporter.report_records()[0].message


def test_reporter_manual_check():
    """Test formatting of reporter using manual and files.
    """
    message = "Hello"
    reporter = Reporter()
    reporter.manual_check(message)
    assert reporter.state() == "manual_check"
    assert message == reporter.report_records()[0].message
    reporter = Reporter()
    reporter.assert_manual_check(False, message)
    assert reporter.state() == "manual_check"
    assert message == reporter.report_records()[0].message


def test_reporter_manual_check_with_file():
    """Test formatting of reporter using manual and files.
    """
    message = "Hello"
    filename = "a.txt"
    reporter = Reporter()
    reporter.manual_check(message, file_name=filename)
    assert reporter.state() == "manual_check"
    assert filename in reporter.report_records()[0].message


def test_reporter_manual_check_with_file_and_line():
    """Test formatting of reporter using manual, files and line.
    """
    message = "Hello"
    filename = "a.txt"
    line_number = 1
    reporter = Reporter()
    reporter.manual_check(message, file_name=filename, line_number=line_number)
    assert reporter.state() == "manual_check"
    assert filename in reporter.report_records()[0].message
    assert str(line_number) in reporter.report_records()[0].message


def test_reporter_not_applicable():
    """Test formatting of reporter using not_applicable.
    """
    message = "Hello"
    reporter = Reporter()
    reporter.not_applicable(message)
    assert reporter.state() == "not_applicable"
    assert message == reporter.report_records()[0].message
    reporter = Reporter()
    reporter.assert_not_applicable(False, message)
    assert reporter.state() == "not_applicable"
    assert message == reporter.report_records()[0].message


def test_reporter_skip():
    """Test formatting of reporter using skip."""
    message = "Not Run"
    reporter = Reporter()
    reporter.skip(message)
    assert reporter.state() == "skipped"
    assert message == reporter.report_records()[0].message


def test_reporter_start():
    """Test start method of reporter."""
    reporter = Reporter()
    reporter.start()
    assert not reporter.metrics["start_time"] is None


def test_reporter_complete_raises_if_start_is_not_called():
    """Test complete method of reporter."""
    with pytest.raises(Exception):
        reporter = Reporter()
        reporter.complete()


def test_reporter_complete():
    """Test complete method of reporter."""
    reporter = Reporter()
    reporter.start()
    reporter.complete()
    assert not reporter.metrics["end_time"] is None


def test_ast_report():
    reporter = Reporter()
    reporter.start()
    base_message = "An item was detected, {}, {}, {}."
    ast_results = {
        'os': [
            {'args': ['\xc0'], 'keywords': {}, 'line_number': 8888},
        ],
    }
    files_with_ast_results = {
        'a.py': ast_results
    }
    massage = base_message.format('os', '?', '')
    reporter._ast_report(massage, files_with_ast_results, reporter.manual_check)
    assert reporter.state() == "manual_check"
    assert massage in reporter.report_records()[0].message
    assert str(8888) in reporter.report_records()[0].message


def test_report_message_file_name_normalization():
    reporter = Reporter()
    test_file_name = r'bin/some_app/some_code.py'
    message_template = (r'The following line will be inspected during code review. '
                        r'The `__builtin__.open` module/method can be used to manipulate files outside of the app dir. '
                        'File: {}.')
    reporter.start()
    reporter.fail(message_template.format(test_file_name),
                  file_name=test_file_name)
    reporter.complete()

    reporter_record = reporter.report_records()[0]
    assert reporter_record.message_filename == test_file_name
    assert reporter_record.message == (r'The following line will be inspected during code review. '
                                       r'The `__builtin__.open` module/method can be used to manipulate files outside of the app dir. '
                                       'File: {}').format(test_file_name)


def test_report_message_file_name_line_number_normalization():
    reporter = Reporter()
    test_file_name = r'bin/some_app/some_code.py'
    test_line_number = r'130'
    message_template = (r'The following line will be inspected during code review. '
                        r'The `__builtin__.open` module/method can be used to manipulate files outside of the app dir. '
                        'File: {}, Line: {}.')
    reporter.start()
    reporter.fail(message_template.format(test_file_name, test_line_number),
                  file_name=test_file_name,
                  line_number=test_line_number)
    reporter.complete()

    reporter_record = reporter.report_records()[0]
    assert reporter_record.message_filename == test_file_name
    assert reporter_record.message_line == test_line_number
    assert reporter_record.message == (r'The following line will be inspected during code review. '
                                       r'The `__builtin__.open` module/method can be used to manipulate files outside of the app dir. '
                                       'File: {} Line Number: {}').format(test_file_name, test_line_number)


def test_report_message_file_name_line_number_normalization_without_params_passing():
    reporter = Reporter()
    test_file_name = r'bin/some_app/some_code.py'
    test_line_number = r'130'
    message_template = (r'The following line will be inspected during code review. '
                        r'The `__builtin__.open` module/method can be used to manipulate files outside of the app dir. '
                        'File: {}, Line: {}.')
    reporter.start()
    reporter.fail(message_template.format(test_file_name, test_line_number))
    reporter.complete()

    reporter_record = reporter.report_records()[0]
    assert reporter_record.message == (r'The following line will be inspected during code review. '
                                       r'The `__builtin__.open` module/method can be used to manipulate files outside of the app dir. '
                                       'File: {} Line Number: {}').format(test_file_name, test_line_number)
