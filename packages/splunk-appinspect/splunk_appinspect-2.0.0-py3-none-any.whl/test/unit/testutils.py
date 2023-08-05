# Copyright 2016 Splunk Inc. All rights reserved.

"""This file is for housing test utility helper classes used to automate the
Splunk AppInspect unit tests for checks.
"""

# Python Standard Libraries
import collections
import csv
import os
import sys
import re
import platform
# Hack so that tests can import splunk_appinspect
myPath = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(myPath, '..', '..'))
# Third-Party Libraries
import pytest
from six import iteritems
# Custom Libraries
import splunk_appinspect


class ScenarioFile(pytest.File):

    def __init__(self, path, parent, packages_dir, resource_manager=None, list_of_groups=None):
        """Constructor Initialization."""
        if resource_manager is None:
            resource_manager = splunk_appinspect.resource_manager.ResourceManager()
        if list_of_groups is None:
            list_of_groups = splunk_appinspect.checks.groups()

        super(ScenarioFile, self).__init__(path, parent)
        self.resource_manager = resource_manager
        self.packages_dir = packages_dir
        self.check_db = collections.defaultdict(dict)

        filename = os.path.split(str(path))[1]
        self.group_name = os.path.splitext(filename)[0].replace('test_', '')

        for group in list_of_groups:
            for check in group.checks():
                self.check_db[group.name][check.name] = check

    def collect(self):
        appgroups = collections.defaultdict(list)
        csvfile = self.fspath.open()
        try:
            for row in csv.DictReader(csvfile):
                appgroups[row['package']].append(row)
        finally:
            csvfile.close()
        for package, rows in iteritems(appgroups):
            package_path = os.path.join(self.packages_dir, package)
            # Build a single context per app package per scenario file
            app = splunk_appinspect.App(package_path)
            for row in rows:
                check = self.check_db[self.group_name].get(
                    row['check'], None)
                name = '{}:{}[{}]'.format(self.group_name,
                                          row['check'],
                                          row['package'])
                yield ScenarioItem(name, self, row, self.resource_manager, check, app)


class ScenarioItem(pytest.Item):
    def __init__(self, name, parent, args, ctx, check, app):
        super(ScenarioItem, self).__init__(name, parent)
        self.args = args
        self.ctx = ctx
        self.check = check
        self.app = app
        self.reporter = None

    def runtest(self):
        assert self.check, "Check {} not found".format(self.name)
        if self.args['included_tags'] is None:
            self.args['included_tags'] = []
        else:
            self.args['included_tags'] = self.args['included_tags'].split(' ')
        with self.ctx.context({
                                'apps': [self.app],
                                'included_tags': self.args['included_tags'],
                                'target_splunk_version': splunk_appinspect.splunk.TargetSplunkVersion(self.args['included_tags']),
                                }) as ctx:
            self.reporter = self.check.run(self.app, resource_manager_context=ctx)

            reports = [(report.message, report.message_filename, report.message_line) for report in self.reporter.report_records(max_records=sys.maxsize)]
            zipped_reports = list(zip(*reports))
            messages = zipped_reports[0] if len(reports) > 0 else ()

            if self.reporter.state() == 'skipped':
                pytest.skip("\n".join(messages))
                return
            expected_result = self.args['expected']
            if self.args['platform'] and self.args['platform'] != "*":
                if platform.system().lower() == "windows" and self.args['platform'].lower() != "windows":
                    pytest.skip("\n".join(messages))
                    return
                if platform.system().lower() in ["darwin", "linux", "unix"] and self.args['platform'].lower() != "unix":
                    pytest.skip("\n".join(messages))
                    return
            error_output = "Expected result of {}, got {}. Messages: {}".format(expected_result, self.reporter.state(), messages)
            assert expected_result == self.reporter.state(), error_output
            if self.args['expect_warnings']:
                is_warning_expected = self.args['expect_warnings'].lower().strip()

                if is_warning_expected == 'true':
                    error_output = ("Warning(s) were expected but not received."
                                    " {}").format(self.name)
                    assert len(self.reporter.warnings()) > 0, error_output
                else:
                    error_output = ("Warning(s) were NOT expected but were"
                                    " received. {}\n"
                                    " Warnings: {}").format(self.name,
                                                            self.reporter.warnings())
                    assert len(self.reporter.warnings()) == 0, error_output

            if len(reports) >= 1 and self.args['expect_filename']:
                from collections import defaultdict
                regex_reports, kwargs_report = defaultdict(set), defaultdict(set)
                for message, filename, lineno in reports:
                    filename_extracted, lineno_extracted = splunk_appinspect.reporter.extract_filename_lineno(message)
                    filename_extracted = filename_extracted.replace('\\', '/') if filename_extracted else ''
                    filename = filename.replace('\\', '/') if filename else ''
                    regex_reports[filename_extracted].add(str(lineno_extracted))
                    kwargs_report[filename].add(str(lineno))
                if regex_reports and kwargs_report:
                    expect_filename = self.args['expect_filename'].strip()
                    expect_lineno = self.args['expect_lineno'].strip() if self.args['expect_lineno'] else ''
                    error_output = "Expected filename: {} and lineno: {} was not matched in reported messages {}"\
                        .format(expect_filename, expect_lineno, reports)

                    if self.args['expect_lineno']:
                        assert all([
                            expect_filename in regex_reports,
                            expect_filename in kwargs_report,
                            expect_lineno in regex_reports[expect_filename],
                            expect_lineno in kwargs_report[expect_filename]]
                        ), error_output
                    else:
                        assert all([
                            expect_filename in regex_reports,
                            expect_filename in kwargs_report]
                        ), error_output
            elif self.args['expect_lineno'] and not self.args['expect_filename']:
                raise Exception("Expected filename is missing!")


