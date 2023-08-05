# Copyright 2018 Splunk Inc. All rights reserved.

# Python Standard Libraries
import sys
import platform
# Third-Party Libraries
# N/A
# Custom Libraries
# N/A


def validate_python_version():
    major, minor, micro, releaselevel, serial = sys.version_info
    version_detected = str(major) + "." + str(minor)

    if (major, minor) < (2, 7):
        # Concatenation is used for python versions < 2.7
        error_output = ("Python version " + version_detected + " was detected."
                        " Splunk AppInspect only supports Python 2.7 +")
        sys.exit(error_output)
    elif platform.system() == "Windows" and (major, minor) > (3, 7):
        error_output = ("Python version " + version_detected + " was detected."
                        " Splunk AppInspect only supports 2.7 <= Python <= 3.7 on Windows.")
        sys.exit(error_output)
