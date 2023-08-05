# Copyright 2018 Splunk Inc. All rights reserved.

"""
### Lookup file standards

Lookups add fields from an external source to events based on the values of fields that are already present in those events.
"""

# Python Standard Library
import logging
import os
import re
import sys
import csv
import glob
# Third-Party Libraries
# N/A
# Custom Libraries
import splunk_appinspect
from splunk_appinspect import lookup

logger = logging.getLogger(__name__)
report_display_order = 13


@splunk_appinspect.tags('splunk_appinspect', 'csv')
@splunk_appinspect.cert_version(min='1.5.0')
def check_lookup_csv_is_valid(app, reporter):
    """Check that `.csv` files are not empty, have at least two columns, have
    headers with no more than 4096 characters, do not use Macintosh-style (\\r)
    line endings, have the same number of columns in every row, and contain
    only UTF-8 characters."""

    for basedir, file, ext in app.iterate_files(basedir="lookups", types=[".csv"]):
        app_file_path = os.path.join(basedir, file)
        full_file_path = app.get_filename(app_file_path)
        try:
            is_valid, rationale = lookup.LookupHelper.is_valid_csv(full_file_path)
            if not is_valid:
                reporter.fail("This .csv lookup is not formatted as valid csv."
                              " Details: {}".format(rationale), app_file_path)
            elif rationale != lookup.VALID_MESSAGE:
                reporter.warn(rationale, app_file_path)
        except Exception as err:
            logger.warn("Error validating lookup. File: {}. Error: {}"
                        .format(full_file_path, err))
            reporter.fail("Error opening and validating lookup. Please"
                          " investigate this lookup and remove it if it is not" 
                          " formatted as valid CSV.", app_file_path)


@splunk_appinspect.tags('cloud')
@splunk_appinspect.cert_version(min='2.0.0')
def check_for_lookups_file_name(app, reporter):
    '''Check that no file/folder under lookups folder is named with ".default" extension.
    When upgrading an App, file/folder will be temporarily renamed with an extra '.default' extension.
    It will run into problems if such a file already exists.
    '''
    if app.directory_exists('lookups'):
        base_dir = os.path.join(app.app_dir, 'lookups')
        for path in glob.glob(base_dir + os.sep + '*.default'):
            file_path = path.replace(app.app_dir, '')
            reporter.fail("The file/directory under lookups folder has an extension of '.default'."
                          " You should remove the '.default' extension.",
                          file_path)
    else:
        reporter.not_applicable('lookups folder does not exist')
