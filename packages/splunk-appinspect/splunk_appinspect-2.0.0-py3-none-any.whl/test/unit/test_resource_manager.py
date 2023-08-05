# Copyright 2016 Splunk Inc. All rights reserved.

# Python Standard Libraries
# N/A
# Third-Party Libraries
import pytest
# Custom Libraries
from splunk_appinspect.resource_manager import ResourceManager, ManagedResource


def test_resource_manager():
    called = {'setup': False, 'release': False}

    class TestManagedResource(ManagedResource):

        def setup(self):
            called['setup'] = True

        def release(self):
            called['release'] = True

        def resource(self):
            return None

    mgr = ResourceManager(test=TestManagedResource)
    with mgr.context() as ctx:
        tst = ctx['test']
        assert not called['release']
    assert called['setup']
    assert called['release']
