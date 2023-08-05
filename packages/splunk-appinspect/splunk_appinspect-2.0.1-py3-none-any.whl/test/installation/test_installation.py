"""A base class for installation testing.

This serves as a mechanism to support shared configurations across multiple
platform requirements via the inheritance paradigm.

usage: `pytest test/installation/test_installation.py`
"""

# Python Standard Libraries
import shutil
import tempfile
import os


# Third-Party Libraries
# N/A
# Custom Libraries
# N/A


class TestInstallationBase(object):
    """A base class to help consolidate platform specific testing into a single
    base class.
    """

    def create_temp_directory(self):
        """Function to help consistent retrieval of a temporary directory to
        work from for testing.

        Returns:
            String: absolute file path to the temporary directory
        """
        self.temporary_directory = tempfile.mkdtemp()
        return self.temporary_directory

    def clean_up_temp_directory(self):
        """Function to cleana up the temporary directory used for testing.

        Returns:
            None
        """
        if self.temporary_directory:
            shutil.rmtree(self.temporary_directory, ignore_errors=True)
        does_temporary_exist_still_exist = os.path.exists(self.temporary_directory)
        assert not does_temporary_exist_still_exist, "clean up of splunk-appinspect testing was not completed!"
