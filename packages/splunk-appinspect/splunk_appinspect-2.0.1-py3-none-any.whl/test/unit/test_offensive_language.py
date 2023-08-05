# Copyright 2016 Splunk Inc. All rights reserved.

# Python Standard Libraries
import os
import pytest
# Custom Libraries
from splunk_appinspect.offense import *


@pytest.mark.skipif(os.name != "posix", reason="Only runs on Linux or OSX platform.")
def test_word_is_profane():
    assert not(word_is_profane('monkey'))
    assert word_is_profane('fuck')
    # Not checking for misspellings- too many false positives with a large word list
    # assert word_is_profane('fukc')
    assert word_is_profane('fucker')
    assert not(word_is_profane('truck'))
    assert not(word_is_profane('tuck'))


@pytest.mark.skipif(os.name != "posix", reason="Only runs on Linux or OSX platform.")
def test_scan_file_clean():
    scriptdir = os.path.dirname(os.path.abspath(__file__))
    results = scan_file(os.path.join(scriptdir, 'data', 'gaffigan.txt'))
    assert len(results) == 0


@pytest.mark.skipif(os.name != "posix", reason="Only runs on Linux or OSX platform.")
def test_scan_file_carlin():
    scriptdir = os.path.dirname(os.path.abspath(__file__))
    results = scan_file(os.path.join(scriptdir, 'data', 'carlin.txt'))
    assert results != []
    known_profane = (
        18, "And words, you know the seven don't you? Shit, Piss, Fuck, Cunt, Cocksucker,", 'Shit', 'shit')
    assert known_profane in results
