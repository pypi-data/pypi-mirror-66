# Copyright 2017 Splunk Inc. All rights reserved.

# Python Standard Libraries
import tempfile
# Third-Party Library
import os
import pytest
# Custom Libraries
from splunk_appinspect import lookup


def _validate_csv_contents(contents):
    """Helper function to create temp file to send to LookupHelper.is_valid_csv()

    Args:
        contents(str): string to fill temp file with to be validated
    Returns:
        True if valid csv
    """
    tmp_file_path = None
    try:
        _, tmp_file_path = tempfile.mkstemp(suffix=".csv")
        with open(tmp_file_path, "wb") as fout:
            fout.write(contents)
            fout.close()
            os.close(_)
        is_valid, rationale = lookup.LookupHelper.is_valid_csv(tmp_file_path)
    finally:
        if tmp_file_path is not None:
            os.unlink(tmp_file_path)
    return is_valid, rationale


def test_lookup_valid_csv():
    """Test a valid csv
    """
    contents = b"one,two,three\n4,5,6"
    is_valid, rationale = _validate_csv_contents(contents)
    assert is_valid == True


def test_lookup_empty():
    """Test an empty csv
    """
    contents = b" \n \t"
    is_valid, rationale = _validate_csv_contents(contents)
    assert is_valid == False
    assert rationale == lookup.LOOKUP_EMPTY_MESSAGE


def test_lookup_one_column():
    """Test a lookup csv with only one column
    """
    contents = b"one\ncolumn"
    is_valid, rationale = _validate_csv_contents(contents)
    assert is_valid


def test_lookup_one_column_with_single_character_row():
    """Test a lookup csv with only one column and with single character in this row,
    this makes it difficult to guess the delimiter
    """
    contents = b"one\nc"
    is_valid, rationale = _validate_csv_contents(contents)
    assert is_valid


def test_lookup_header_too_large():
    """Test a csv with a header over the character limit
    """
    contents = "column"
    row = "0"
    while len(contents) <= lookup.LOOKUP_HEADER_CHAR_LIMIT:
        contents += ",column"
        row += ",0"
    contents += "\n" + row
    is_valid, rationale = _validate_csv_contents(contents.encode())
    assert is_valid == False
    assert rationale == lookup.LOOKUP_HEADER_CHAR_LIMIT_MESSAGE


def test_lookup_carriage_return_line_endings():
    """Test a csv with \\r line endings
    """
    contents = b"one,two,three\r4,5,6"
    is_valid, rationale = _validate_csv_contents(contents)
    assert is_valid is True
    assert rationale == lookup.LOOKUP_MAC_LINE_ENDINGS_MESSAGE


def test_lookup_rows_with_different_number_of_columns():
    """Test a csv with rows that have varying numbers of columns
    """
    contents = b"one,two,three\n4,5,6,7,8"
    is_valid, rationale = _validate_csv_contents(contents)
    assert is_valid == False
    assert rationale == lookup.LOOKUP_COLUMN_MISMATCH_MESSAGE.format(2, 5, 3)
    contents = b"one,two,three,four\n1,2,3,4\n4,5"
    is_valid, rationale = _validate_csv_contents(contents)
    assert is_valid == False
    assert rationale == lookup.LOOKUP_COLUMN_MISMATCH_MESSAGE.format(3, 2, 4)


def test_non_utf8_chars():
    """Test a csv with non-utf8 characters
    """
    contents = b"one,\xe2,three\n4,5,6"
    is_valid, rationale = _validate_csv_contents(contents)
    assert is_valid == False
    assert rationale == lookup.LOOKUP_NON_UTF8_MESSAGE
