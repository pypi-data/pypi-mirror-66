# Copyright 2017 Splunk Inc. All rights reserved.

# Python Standard Libraries
# Third-Party Library
# Custom Libraries
from splunk_appinspect.documentation import DocumentationLinks


def test_get_splunk_docs_link_when_link_exists():
    """Test a link exists for a known conf file."""
    links = DocumentationLinks()
    link = links.get_splunk_docs_link("app.conf")
    assert "http" in link


def test_get_splunk_docs_link_when_link_does_not_exist():
    """Test link does not exist for an unknown file."""
    links = DocumentationLinks()
    link = links.get_splunk_docs_link("blah.conf")
    assert "Unable to find" in link
