"""This could be considered a facade to provide simple access to
splunk-appinspect builds for testing.
"""

# Copyright 2017 Splunk Inc. All rights reserved.

# Python Standard Libraries
import logging
import os
import shutil
import subprocess
import tempfile
from six.moves.urllib.request import urlretrieve


# Third-Party Libraries
# N/A
# Custom Libraries
from test.installation.util import copy_directory

logger = logging.getLogger(__name__)

current_directory = os.path.dirname(os.path.abspath(__file__))
repository_root_directory = os.path.abspath(os.path.join(current_directory, "..", ".."))


class SplunkAppInspectURLNotFoundException(Exception):
    """An error to call out when we're trying to retrieve a build of
    splunk-appinspect that does not exist.
    """
    pass


class SplunkAppInspectVersionNotSupportedException(Exception):
    """An error to call out a version of splunk-appinspect that is not yet
    supported for retrieval.
    """
    pass


class SplunkAppInspectBuilds(object):
    """A class that serves to provide a simple interface for retrieving
    splunk-appinspect builds.
    """

    def __init__(self):
        """Constructor. Performs setup method because this isn't reliably
        integrated into pytest such that it can be created as a fixture and
        passed to each test accordingly. In an ideal environment this would only
        be created once and passed around many times.
        """
        self.setup_method()

    def setup_method(self):
        """Setup method."""

        # If a version isn't in this url, then it's 'not supported'
        self.__splunk_appinspect_urls = {
            "latest": "This is not used",
            "1.5.0": "https://repo.splunk.com/artifactory/Solutions/AppInspect/CLI/master/builds/140/splunk-appinspect-1.5.0.140.tar.gz",
            "1.5.1": "https://repo.splunk.com/artifactory/Solutions/AppInspect/CLI/master/builds/141/splunk-appinspect-1.5.1.141.tar.gz",
            "1.5.2": "https://repo.splunk.com/artifactory/Solutions/AppInspect/CLI/master/builds/142/splunk-appinspect-1.5.2.142.tar.gz",
        }

        self.__cached_appinspect_builds = dict()

        self.__temporary_directory = tempfile.mkdtemp()
        self.__build_directory_path = os.path.join(self.__temporary_directory, "splunk_appinspect_builds")

        logger.info(("Temporary working directory for AppInspect Builds: {}")
                    .format(self.__temporary_directory))

    def teardown_method(self):
        """Teardown method. This must be called manually within the testing area
        to ensure that this gets performed. This is done because there was not a
        reliable way to get pytest to teardown fixtures used for testing.
        """
        shutil.rmtree(self.__temporary_directory, ignore_errors=True)

    def _clean_sdist_build(self, env):
        """Copies the repository to a temporary location, performs the `python
        setup.py sdist` and then returns the path to the generated artifact.

        Arguments:
            env (String?): The environment context with which to perform the
                build commands with

        Returns:
            String: The absolute file path to the build artifact that was
                generated
        """

        # Create build directory
        temporary_build_directory = os.path.join(self.__temporary_directory,
                                                 "splunk_appinspect_sdist_build")
        distribution_directory = os.path.join(temporary_build_directory,
                                              "dist")
        if os.path.exists(temporary_build_directory):
            shutil.rmtree(temporary_build_directory)

        # Copy build source over
        copy_directory(repository_root_directory, temporary_build_directory)

        # Begin build of artifact
        if os.path.exists(distribution_directory):
            shutil.rmtree(distribution_directory)

        return_value = subprocess.check_output(["python", "setup.py", "sdist"],
                                               env=env,
                                               cwd=temporary_build_directory)

        distribution_directory_contents = os.listdir(distribution_directory)

        # Just to confirm that only the build has been created
        artifact_error_message = ("The output for the `python setup.py sdist`"
                                  " command has resulted in unanticipated"
                                  " results. There should be only one artifact"
                                  " generated. From this process."
                                  " Directory: {}"
                                  " File(s) detected: {}").format(distribution_directory,
                                                                  distribution_directory_contents)
        assert return_value != 0, "Unexpected result for the `python setup.py sdist` command."
        assert len(distribution_directory_contents) == 1, artifact_error_message

        clean_splunk_appinspect_build_path = os.path.join(distribution_directory,
                                                          distribution_directory_contents[0])
        return clean_splunk_appinspect_build_path

    def get_splunk_appinspect_download_url(self, version):
        """Helper function to perform error raising for un-supported versions
        of artifacts.

        Arguments:
            version (String): The version to retrieve

        Returns:
            None
        """
        is_version_available = version in self.__splunk_appinspect_urls

        if is_version_available:
            return self.__splunk_appinspect_urls[version]
        else:
            raise SplunkAppInspectURLNotFoundException

    def download_splunk_appinspect(self, directory_location, version):
        """Retrieves splunk-appinspect from external systems and places them in
        a temporary location for retrieval.

        Arguments:
            directory_location (String): Absolute file path to directory that
                the downloaded arifact will be placed in.
            version (String): The version of the artifact to download

        Returns:
            String: The absolute file path to the artifact that was downloaded.
        """
        # Generalize to be adapters for specific resources???
        cleaned_version = version.replace(".", "_")
        file_name = "splunk_appinspect_{}.tar.gz".format(cleaned_version)
        file_path = os.path.join(directory_location, file_name)

        download_url = self.get_splunk_appinspect_download_url(version)

        urlretrieve(download_url, file_path)

        # Do we want to error catch here for the artifact?
        # What should be checked?
        return file_path

    def retrieve_splunk_appinspect_path(self, version, env):
        """Retrieves the absolute path to the artifact that will be used.

        Arguments:
            version (String): Must be in major.minor.patch
            env (String?): The environment context with which to perform the
                retrieval with

        Returns:
            (String): The absolute path to splunk-appinspect version artifact
                specified
        """
        is_version_available = version in self.__splunk_appinspect_urls
        is_version_already_cached = (is_version_available and
                                     version in self.__cached_appinspect_builds and
                                     self.__cached_appinspect_builds[version] is not None)

        if not is_version_available:
            raise SplunkAppInspectVersionNotSupportedException

        if is_version_already_cached:
            # __build_directory_path = os.path.join(__temporary_directory, "splunk_appinspect_builds")
            return self.__cached_appinspect_builds[version]
        else:
            if version == "latest":
                splunk_appinspect_file_path = self._clean_sdist_build(env)
            else:
                splunk_appinspect_file_path = self.download_splunk_appinspect(self.__temporary_directory,
                                                                              version)

            self.__cached_appinspect_builds[version] = splunk_appinspect_file_path
            return splunk_appinspect_file_path
