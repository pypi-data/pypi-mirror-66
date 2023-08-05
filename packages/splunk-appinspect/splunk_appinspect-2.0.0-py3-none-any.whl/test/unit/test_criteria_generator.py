"""This is the unit testing for the criteria_generator.py module

usage: 'pytest test/unit/test_criteria_generator.py'
"""
# Python Standard Libraries
import datetime
# Third-Party Libraries
# N/A
# Custom Libraries
import splunk_appinspect


def test_generate_critera_as_html_has_the_correct_version():
    """Test that the correct date exists in the html markup generated. Does not
    account for the html formatting.
    """
    html_markup_criteria = splunk_appinspect.documentation.criteria_generator.generate_critera_as_html()

    current_date = datetime.datetime.now()
    formatted_current_date = current_date.strftime("%d %B, %Y")

    assert formatted_current_date in html_markup_criteria


def test_generate_critera_as_html_has_the_correct_date():
    """Test that the correct date version in the html markup generated. Does not
    account for the html formatting.
    """
    html_markup_criteria = splunk_appinspect.documentation.criteria_generator.generate_critera_as_html()

    assert splunk_appinspect.version.__version__ in html_markup_criteria


def test_generate_critera_as_html_has_the_correct_tags():
    """Test that the correct tags exist in the html markup generated. Does not
    account for the html formatting.
    """
    included_tags = ["splunk_appinspect", "cloud"]

    html_markup_criteria = splunk_appinspect.documentation.criteria_generator.generate_critera_as_html(included_tags=included_tags)

    # Per docs, we have hardcoded the html to be splunk_<br>appinspect for
    # splunk_appinspect so that the column is not too wide
    formatted_tags = ["splunk_<br>appinspect", "cloud"]
    for tag in formatted_tags:
        assert tag in html_markup_criteria
