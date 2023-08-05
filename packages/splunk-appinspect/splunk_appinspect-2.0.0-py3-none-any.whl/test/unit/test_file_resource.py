# Copyright 2017 Splunk Inc. All rights reserved.

# Python Standard Libraries
import os

from splunk_appinspect.file_resource import FileResource

def test_xml_file_resource():
    valid_xml_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'data', 'sample.xml')
    xml_resource = FileResource(valid_xml_path)
    assert xml_resource
    assert xml_resource.parse('xml')