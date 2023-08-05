#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import json
from xml.dom import minidom
from xml.parsers.expat import ExpatError

import lxml.etree as et
import pytest
from builtins import str as text

from splunk_appinspect.formatters.validation_report_json_formatter import ValidationReportJSONFormatter
from splunk_appinspect.formatters.validation_report_junitxml_formatter import ValidationReportJUnitXMLFormatter
from splunk_appinspect.validation_report import ValidationReport


def test_validation_report_junitxml_formatter():
    """Test junitxml formatter output is (str, unicode) for stdout"""
    junit_report_formatter = ValidationReportJUnitXMLFormatter()
    result = junit_report_formatter.format(validation_report=ValidationReport())
    assert isinstance(result, text)
    assert et.XML(result.encode('utf-8')).tag == 'testsuites'


def test_validation_report_json_formatter():
    """Test json formatter output is str for stdout"""
    json_report_formatter = ValidationReportJSONFormatter()
    result = json_report_formatter.format(validation_report=ValidationReport())
    assert isinstance(result, str)
    assert isinstance(json.loads(result), dict)


def test_stdlib_minidom_prettify_failure():
    # This is to prove stdlib `minidom.parseString` will certainly fail on bad xml char like `&`
    test_raw_xml_string = """<?xml version="1.0" encoding="UTF-8"?><view><title>A & B</title></view>"""
    with pytest.raises(ExpatError, match=r'not well-formed'):
        assert minidom.parseString(test_raw_xml_string).toprettyxml()
