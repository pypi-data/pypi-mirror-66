# Copyright 2016 Splunk Inc. All rights reserved.

# Python Standard Libraries
import os
import re
import pytest
from splunk_appinspect.image_resource import ImageResource


def test_parse_png_dimension():
    preview_png_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'data', 'sample.png')
    png_resource = ImageResource(preview_png_path)
    dims = png_resource.dimensions()
    assert dims[0] == 256 and dims[1] == 128


def test_parse_png_content_type():
    preview_png_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'data', 'sample.png')
    png_resource = ImageResource(preview_png_path)
    assert png_resource.is_png()
    assert png_resource.content_type() == 'PNG'


def test_parse_invalid_png_dimension():
    preview_png_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'data', 'invalid.png')
    with pytest.raises(IOError):
        png_resource = ImageResource(preview_png_path)
        png_resource.dimensions()
