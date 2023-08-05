# Copyright 2018 Splunk Inc. All rights reserved.

"""
### Deprecated features from Splunk Enterprise 7.2

The following features should not be supported in Splunk 7.2 or later. For more, see <a href="http://docs.splunk.com/Documentation/Splunk/7.2.0/ReleaseNotes/Deprecatedfeatures" target="_blank">Deprecated features</a> and <a href="http://docs.splunk.com/Documentation/Splunk/latest/Installation/ChangesforSplunkappdevelopers" target="_blank">Changes for Splunk App developers</a>.
"""

# Python Standard Libraries
import logging

# Third-Party Libraries
import bs4

# Custom Libraries
import splunk_appinspect
from splunk_appinspect.check_routine import blacklist_conf

logger = logging.getLogger(__name__)


@splunk_appinspect.tags("splunk_appinspect", "splunk_7_2", "deprecated_feature")
@splunk_appinspect.cert_version(min="1.7.0")
def check_for_deprecated_literals_conf(app, reporter):
    """
    Check deprecated literals.conf existence.
    """
    blacklist_conf(app, reporter.warn, 'literals.conf',
                   'literals.conf has been deprecated in Splunk 7.2. '
                   'Please use messages.conf instead.')
