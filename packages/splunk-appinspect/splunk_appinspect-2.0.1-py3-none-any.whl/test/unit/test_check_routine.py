import splunk_appinspect
from splunk_appinspect import check_routine
import pytest
import os


APPINSPECT_TEST_PATH = os.path.dirname(os.path.abspath(__file__))
APPINSPECT_TEST_PACKAGES_PATH = os.path.join(APPINSPECT_TEST_PATH, "packages", "has_findtypes_command_ACD-3118")


@pytest.mark.parametrize('app_package,command,expected_findings', [
    (os.path.join(APPINSPECT_TEST_PACKAGES_PATH, 'has_findtypes_in_savedsearches'), 'findtypes',
        [(os.path.join('default', 'savedsearches.conf'), 2)],
    ),
    (os.path.join(APPINSPECT_TEST_PACKAGES_PATH, 'has_findtypes_in_dashboard_view'), 'findtypes',
        [(os.path.join('default', 'data', 'ui', 'views', 'example.xml'), None)],
    )
])
def test_find_spl_command_usage(app_package, command, expected_findings):
    app = splunk_appinspect.App(app_package)
    findings = check_routine.find_spl_command_usage(app, command)
    assert expected_findings == findings


@pytest.mark.parametrize('xml_files,nodes,expected_findings_text', [
    ([(os.path.join('default', 'data', 'ui', 'views', 'example.xml'),
        os.path.join(APPINSPECT_TEST_PACKAGES_PATH, 'has_findtypes_in_dashboard_view', 'default', 'data', 'ui', 'views', 'example.xml'),
        )
     ], [check_routine.xml_node('title')], 'Log events'),
])
def test_util_find_xml_nodes_usages(xml_files, nodes, expected_findings_text):
    findings = check_routine.util.find_xml_nodes_usages(xml_files, nodes)
    assert expected_findings_text == findings[0][0].text