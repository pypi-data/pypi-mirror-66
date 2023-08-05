"""Copyright 2017 Splunk Inc. All rights reserved."""

# Python Standard Libraries
import imp
import json
import os
# Third-Party Library
# Custom Libraries
import splunk_appinspect
from splunk_appinspect.validation_report import ApplicationValidationReport
from splunk_appinspect.validation_report import ValidationReport
from splunk_appinspect.app import App


APP_PACKAGES = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'packages', 'app_package_testing_packages')
PACKAGES = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'packages')
GOOD_TGZ = os.path.join(APP_PACKAGES, 'good_app_conf.tgz')


def test_validation_report_init():
    """Test setup of the ValidationReport."""
    report = ValidationReport()
    assert report


def test_app_validation_report_init():
    """Test setup of the ApplicationValidationReport."""
    good_app = App(GOOD_TGZ)
    report = ApplicationValidationReport(good_app, None)
    assert report


def test_validation_report_summary_empty():
    """Test get_summary() failure results in ValidationReport."""
    app = App(GOOD_TGZ)
    validation_report = ValidationReport()
    summary_dict = json.loads(json.dumps(validation_report.get_summary()))
    expected_dict = {}
    assert summary_dict == expected_dict


def test_validation_report_summary_failures():
    """Test get_summary() failure results in ValidationReport."""
    app = App(GOOD_TGZ)
    validation_report = ValidationReport()

    # Fail some checks
    @splunk_appinspect.tags("foobar")
    def test_check_fail(app, reporter):
        reporter.fail("Blah.")

    test_group_name = "test.module.name"
    test_module = imp.new_module(test_group_name)
    test_module.check_test_one = test_check_fail
    test_module.check_test_two = test_check_fail
    test_group = splunk_appinspect.checks.generate_group(test_module)

    results = []
    for c in test_group.checks():
        reporter = c.run(app)
        results.append((test_group, c, reporter))
    report = ApplicationValidationReport(app, None)
    report.results = results

    validation_report.add_application_validation_report(report)
    assert validation_report.application_validation_reports[0] == report
    summary_dict = json.loads(json.dumps(validation_report.get_summary()))
    expected_dict = {
        u'error': 0,
        u'failure': 2,
        u'manual_check': 0,
        u'not_applicable': 0,
        u'skipped': 0,
        u'success': 0,
        u'warning': 0
    }
    assert summary_dict == report.get_summary() == expected_dict


def test_validation_report_summary_manual_checks():
    """Test get_summary() manual check results in ValidationReport."""
    app = App(GOOD_TGZ)
    validation_report = ValidationReport()

    # Manual check some checks
    @splunk_appinspect.tags("foobar")
    def test_check_mc(app, reporter):
        reporter.manual_check("Blah.")

    test_group_name = "test.module.name"
    test_module = imp.new_module(test_group_name)
    test_module.check_test_one = test_check_mc
    test_group = splunk_appinspect.checks.generate_group(test_module)

    results = []
    for c in test_group.checks():
        reporter = c.run(app)
        results.append((test_group, c, reporter))
    report = ApplicationValidationReport(app, None)
    report.results = results

    validation_report.add_application_validation_report(report)
    assert validation_report.application_validation_reports[0] == report
    summary_dict = json.loads(json.dumps(validation_report.get_summary()))
    expected_dict = {
        u'error': 0,
        u'failure': 0,
        u'manual_check': 1,
        u'not_applicable': 0,
        u'skipped': 0,
        u'success': 0,
        u'warning': 0
    }
    assert summary_dict == report.get_summary() == expected_dict


def test_validation_report_summary_errors():
    """Test get_summary() error results in ValidationReport."""
    app = App(GOOD_TGZ)
    validation_report = ValidationReport()

    # Error some checks
    @splunk_appinspect.tags("foobar")
    def test_check_error(app, reporter):
        raise Exception("Oops")

    test_group_name = "test.module.name"
    test_module = imp.new_module(test_group_name)
    test_module.check_test_one = test_check_error
    test_module.check_test_two = test_check_error
    test_module.check_test_three = test_check_error
    test_group = splunk_appinspect.checks.generate_group(test_module)

    results = []
    for c in test_group.checks():
        reporter = c.run(app)
        results.append((test_group, c, reporter))
    report = ApplicationValidationReport(app, None)
    report.results = results

    validation_report.add_application_validation_report(report)
    assert validation_report.application_validation_reports[0] == report
    summary_dict = json.loads(json.dumps(validation_report.get_summary()))
    expected_dict = {
        u'error': 3,
        u'failure': 0,
        u'manual_check': 0,
        u'not_applicable': 0,
        u'skipped': 0,
        u'success': 0,
        u'warning': 0
    }
    assert summary_dict == report.get_summary() == expected_dict


def test_validation_report_summary_na():
    """Test get_summary() N/A results in ValidationReport."""
    app = App(GOOD_TGZ)
    validation_report = ValidationReport()

    # N/A some checks
    @splunk_appinspect.tags("foobar")
    def test_check_na(app, reporter):
        reporter.not_applicable("Blah.")

    test_group_name = "test.module.name"
    test_module = imp.new_module(test_group_name)
    test_module.check_test_one = test_check_na
    test_module.check_test_two = test_check_na
    test_group = splunk_appinspect.checks.generate_group(test_module)

    results = []
    for c in test_group.checks():
        reporter = c.run(app)
        results.append((test_group, c, reporter))
    report = ApplicationValidationReport(app, None)
    report.results = results

    validation_report.add_application_validation_report(report)
    assert validation_report.application_validation_reports[0] == report
    summary_dict = json.loads(json.dumps(validation_report.get_summary()))
    expected_dict = {
        u'error': 0,
        u'failure': 0,
        u'manual_check': 0,
        u'not_applicable': 2,
        u'skipped': 0,
        u'success': 0,
        u'warning': 0
    }
    assert summary_dict == report.get_summary() == expected_dict


def test_validation_report_summary_skip():
    """Test get_summary() skip results in ValidationReport."""
    app = App(GOOD_TGZ)
    validation_report = ValidationReport()

    # Skip some checks
    @splunk_appinspect.tags("foobar")
    def test_check_skip(app, reporter):
        reporter.skip("Blah.")

    test_group_name = "test.module.name"
    test_module = imp.new_module(test_group_name)
    test_module.check_test_one = test_check_skip
    test_group = splunk_appinspect.checks.generate_group(test_module)

    results = []
    for c in test_group.checks():
        reporter = c.run(app)
        results.append((test_group, c, reporter))
    report = ApplicationValidationReport(app, None)
    report.results = results

    validation_report.add_application_validation_report(report)
    assert validation_report.application_validation_reports[0] == report
    summary_dict = json.loads(json.dumps(validation_report.get_summary()))
    expected_dict = {
        u'error': 0,
        u'failure': 0,
        u'manual_check': 0,
        u'not_applicable': 0,
        u'skipped': 1,
        u'success': 0,
        u'warning': 0
    }
    assert summary_dict == report.get_summary() == expected_dict


def test_validation_report_summary_success():
    """Test get_summary() success results in ValidationReport."""
    app = App(GOOD_TGZ)
    validation_report = ValidationReport()

    # Success some checks
    @splunk_appinspect.tags("foobar")
    def test_check_success(app, reporter):
        pass

    test_group_name = "test.module.name"
    test_module = imp.new_module(test_group_name)
    test_module.check_test_one = test_check_success
    test_module.check_test_two = test_check_success
    test_module.check_test_three = test_check_success
    test_module.check_test_four = test_check_success
    test_module.check_test_five = test_check_success
    test_group = splunk_appinspect.checks.generate_group(test_module)

    results = []
    for c in test_group.checks():
        reporter = c.run(app)
        results.append((test_group, c, reporter))
    report = ApplicationValidationReport(app, None)
    report.results = results

    validation_report.add_application_validation_report(report)
    assert validation_report.application_validation_reports[0] == report
    summary_dict = json.loads(json.dumps(validation_report.get_summary()))
    expected_dict = {
        u'error': 0,
        u'failure': 0,
        u'manual_check': 0,
        u'not_applicable': 0,
        u'skipped': 0,
        u'success': 5,
        u'warning': 0
    }
    assert summary_dict == report.get_summary() == expected_dict


def test_validation_report_summary_warn():
    """Test get_summary() warn results in ValidationReport."""
    app = App(GOOD_TGZ)
    validation_report = ValidationReport()

    # Warn some checks
    @splunk_appinspect.tags("foobar")
    def test_check_warn(app, reporter):
        reporter.warn("Blah.")

    test_group_name = "test.module.name"
    test_module = imp.new_module(test_group_name)
    test_module.check_test_one = test_check_warn
    test_module.check_test_two = test_check_warn
    test_module.check_test_three = test_check_warn
    test_module.check_test_four = test_check_warn
    test_group = splunk_appinspect.checks.generate_group(test_module)

    results = []
    for c in test_group.checks():
        reporter = c.run(app)
        results.append((test_group, c, reporter))
    report = ApplicationValidationReport(app, None)
    report.results = results

    validation_report.add_application_validation_report(report)
    assert validation_report.application_validation_reports[0] == report
    summary_dict = json.loads(json.dumps(validation_report.get_summary()))
    expected_dict = {
        u'error': 0,
        u'failure': 0,
        u'manual_check': 0,
        u'not_applicable': 0,
        u'skipped': 0,
        u'success': 0,
        u'warning': 4
    }
    assert summary_dict == report.get_summary() == expected_dict


def _make_application_validation_report_multiple_results():
    """Helper function to make ValidationReport with NA/Skip/Success/Warn
    results."""
    app = App(GOOD_TGZ)

    # NA/Skip/Success/Warn some checks
    @splunk_appinspect.tags("foobar")
    def test_check_na(app, reporter):
        reporter.not_applicable("Blah.")

    @splunk_appinspect.tags("foobar")
    def test_check_skip(app, reporter):
        reporter.skip("Blah.")

    @splunk_appinspect.tags("foobar")
    def test_check_success(app, reporter):
        pass

    @splunk_appinspect.tags("foobar")
    def test_check_warn(app, reporter):
        reporter.warn("Blah.")

    test_na_module = imp.new_module("test.na_group")
    test_na_module.check_test_one = test_check_na
    test_na_module.check_test_two = test_check_na
    test_na_module.check_test_three = test_check_na
    test_na_module.check_test_four = test_check_na
    test_na_group = splunk_appinspect.checks.generate_group(test_na_module)

    test_skip_module = imp.new_module("test.skip_group")
    test_skip_module.check_test_five = test_check_skip
    test_skip_module.check_test_six = test_check_skip
    test_skip_module.check_test_seven = test_check_skip
    test_skip_group = splunk_appinspect.checks.generate_group(test_skip_module)

    test_success_module = imp.new_module("test.success_group")
    test_success_module.check_test_eight = test_check_success
    test_success_module.check_test_nine = test_check_success
    test_success_group = splunk_appinspect.checks.generate_group(test_success_module)

    test_warn_module = imp.new_module("test.warn_group")
    test_warn_module.check_test_ten = test_check_warn
    test_warn_group = splunk_appinspect.checks.generate_group(test_warn_module)

    results = []
    for test_group in [test_na_group, test_skip_group, test_success_group,
                       test_warn_group]:
        for c in test_group.checks():
            reporter = c.run(app)
            results.append((test_group, c, reporter))
    report = ApplicationValidationReport(app, None)
    report.results = results

    return report


def test_validation_report_summary_multiple_results():
    """Test get_summary() NA/Skip/Success/Warn results in ValidationReport."""
    validation_report = ValidationReport()
    report = _make_application_validation_report_multiple_results()
    validation_report.add_application_validation_report(report)
    assert validation_report.application_validation_reports[0] == report
    summary_dict = json.loads(json.dumps(validation_report.get_summary()))
    expected_dict = {
        u'error': 0,
        u'failure': 0,
        u'manual_check': 0,
        u'not_applicable': 4,
        u'skipped': 3,
        u'success': 2,
        u'warning': 1
    }
    assert summary_dict == report.get_summary() == expected_dict


def test_application_validation_report_groups():
    """Test ApplicationValidationReport.groups() output"""
    report = _make_application_validation_report_multiple_results()
    group_list = [(res[0].name, res[1].name, res[2].state())
                  for lst in report.groups() for res in lst]
    expected_group_list = [
        ('test.na_group', 'check_test_four', 'not_applicable'),
        ('test.na_group', 'check_test_one', 'not_applicable'),
        ('test.na_group', 'check_test_three', 'not_applicable'),
        ('test.na_group', 'check_test_two', 'not_applicable'),
        ('test.skip_group', 'check_test_five', 'skipped'),
        ('test.skip_group', 'check_test_seven', 'skipped'),
        ('test.skip_group', 'check_test_six', 'skipped'),
        ('test.success_group', 'check_test_eight', 'success'),
        ('test.success_group', 'check_test_nine', 'success'),
        ('test.warn_group', 'check_test_ten', 'warning')
    ]
    assert group_list == expected_group_list


def test_validation_report_multiple_application_reports():
    """Test get_summary() for multiple ApplicationValidationReports in
    ValidationReport."""
    validation_report = ValidationReport()
    report0 = _make_application_validation_report_multiple_results()
    report1 = _make_application_validation_report_multiple_results()
    report2 = _make_application_validation_report_multiple_results()
    validation_report.add_application_validation_report(report0)
    assert validation_report.application_validation_reports[0] == report0
    summary_dict = json.loads(json.dumps(validation_report.get_summary()))
    expected_dict = {
        u'error': 0,
        u'failure': 0,
        u'manual_check': 0,
        u'not_applicable': 4,
        u'skipped': 3,
        u'success': 2,
        u'warning': 1
    }
    assert (summary_dict == report0.get_summary() == report1.get_summary() ==
            report2.get_summary() == expected_dict)
    validation_report.add_application_validation_report(report1)
    assert validation_report.application_validation_reports[0] == report0
    assert validation_report.application_validation_reports[1] == report1
    summary_dict = json.loads(json.dumps(validation_report.get_summary()))
    expected_dict = {
        u'error': 0,
        u'failure': 0,
        u'manual_check': 0,
        u'not_applicable': 8,
        u'skipped': 6,
        u'success': 4,
        u'warning': 2
    }
    assert summary_dict == expected_dict
    validation_report.add_application_validation_report(report2)
    assert validation_report.application_validation_reports[0] == report0
    assert validation_report.application_validation_reports[1] == report1
    assert validation_report.application_validation_reports[2] == report2
    summary_dict = json.loads(json.dumps(validation_report.get_summary()))
    expected_dict = {
        u'error': 0,
        u'failure': 0,
        u'manual_check': 0,
        u'not_applicable': 12,
        u'skipped': 9,
        u'success': 6,
        u'warning': 3
    }
    assert summary_dict == expected_dict


def test_validation_report_has_invalid_packages_when_check_fails():
    """Test setup of the ApplicationValidationReport."""

    @splunk_appinspect.tags("packaging_standards")
    def test_check(app, reporter):
        reporter.fail("Blah.")

    test_group_name = "test.module.name"
    test_module = imp.new_module(test_group_name)
    test_module.check_test_one = test_check
    test_group = splunk_appinspect.checks.generate_group(test_module)

    app = App(GOOD_TGZ)
    report = ApplicationValidationReport(app, None)

    for c in test_group.checks():
        reporter = c.run(app)
        report.results = [(test_group, c, reporter)]

    validation_report = ValidationReport()
    validation_report.add_application_validation_report(report)
    assert validation_report.application_validation_reports[0] == report
    assert validation_report.has_invalid_packages
    summary_dict = json.loads(json.dumps(validation_report.get_summary()))
    expected_dict = {
        u'error': 0,
        u'failure': 1,
        u'manual_check': 0,
        u'not_applicable': 0,
        u'skipped': 0,
        u'success': 0,
        u'warning': 0
    }
    assert summary_dict == expected_dict


def test_app_validation_report_has_invalid_package_when_check_errors():
    """Test setup of the ApplicationValidationReport."""

    @splunk_appinspect.tags("packaging_standards")
    def test_check():
        raise Exception

    test_group_name = "test.module.name"
    test_module = imp.new_module(test_group_name)
    test_module.check_test_one = test_check
    test_group = splunk_appinspect.checks.generate_group(test_module)

    app = App(GOOD_TGZ)
    report = ApplicationValidationReport(app, None)

    for c in test_group.checks():
        reporter = c.run(app)
        report.results = [(test_group, c, reporter)]

    assert report.has_invalid_package


def test_app_validation_report_has_invalid_package_when_check_fails():
    """Test setup of the ApplicationValidationReport."""

    @splunk_appinspect.tags("packaging_standards")
    def test_check(app, reporter):
        reporter.fail("Blah.")

    test_group_name = "test.module.name"
    test_module = imp.new_module(test_group_name)
    test_module.check_test_one = test_check
    test_group = splunk_appinspect.checks.generate_group(test_module)

    app = App(GOOD_TGZ)
    report = ApplicationValidationReport(app, None)

    for c in test_group.checks():
        reporter = c.run(app)
        report.results = [(test_group, c, reporter)]

    assert report.has_invalid_package


def test_app_validation_report_has_valid_package_when_check_passes():
    """Test setup of the ApplicationValidationReport."""

    @splunk_appinspect.tags("packaging_standards")
    def test_check():
        pass

    test_group_name = "test.module.name"
    test_module = imp.new_module(test_group_name)
    test_module.check_test_one = test_check
    test_group = splunk_appinspect.checks.generate_group(test_module)

    app = App(GOOD_TGZ)
    report = ApplicationValidationReport(app, None)

    for c in test_group.checks():
        reporter = c.run(app)
        report.results = [(test_group, c, reporter)]

    assert not report.has_invalid_package
