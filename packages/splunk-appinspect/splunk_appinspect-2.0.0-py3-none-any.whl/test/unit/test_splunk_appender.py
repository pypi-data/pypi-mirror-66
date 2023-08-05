#!/usr/bin/env python

# Copyright 2016 Splunk Inc. All rights reserved.

"""A quick test script for the Splunk Event Handler logger."""

# Python Standard Libraries
import logging
import socket
# Third-Party Libraries
import pytest
# Custom Libraries
import splunk_appinspect.infra


logger = splunk_appinspect.infra.log_utils.create_logger()
logger.debug("debug")
logger.info("info")
logger.warning("warn")
logger.error("error")
