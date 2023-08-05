from splunk_appinspect.python_modules_metadata.metadata_common import metadata_consts
from splunk_appinspect.python_modules_metadata.python_modules_metadata_store import metadata_store

from hamcrest import *


def test_module_importing_tag():
    objects = metadata_store.query().tag(metadata_consts.TagConsts.MODULE_IMPORTING).collect()
    assert_that(objects, has_length(greater_than(0)))
    names = [o.namespace for o in objects]
    assert_that(names, has_item('imp.load_module'))
    assert_that(names, has_item('importlib.import_module'))
    assert_that(names, has_item('zipimport.zipimporter'))
    assert_that(names, has_item('pkgutil.ImpImporter.find_module'))
    assert_that(names, has_item('pkgutil.ImpLoader.load_module'))
    assert_that(names, has_item('imputil.Importer'))
    assert_that(names, has_item('imputil.BuiltinImporter'))
    assert_that(names, has_item('modulefinder.ReplacePackage'))
    assert_that(names, has_item('modulefinder.ModuleFinder.run_script'))
    assert_that(names, has_item('runpy.run_module'))
    assert_that(names, has_item('runpy.run_path'))


def test_network_connection_tag():
    objects = metadata_store.query().tag(metadata_consts.TagConsts.NETWORK_CONNECTION).collect()
    assert_that(objects, has_length(greater_than(0)))
