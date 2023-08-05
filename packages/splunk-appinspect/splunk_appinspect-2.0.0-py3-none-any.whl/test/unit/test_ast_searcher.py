from hamcrest import *

from splunk_appinspect.python_modules_metadata.python_modules_metadata_store import metadata_store
from splunk_appinspect.check_routine.python_ast_searcher.ast_searcher import AstSearcher
from os.path import dirname, join, abspath

from splunk_appinspect.python_modules_metadata.metadata_common import metadata_consts
from splunk_appinspect.python_analyzer.client import Client
from splunk_appinspect.python_analyzer.trustedlibs.utilities import get_hash_file

APPINSPECT_TEST_PATH = dirname(abspath(__file__))

APPINSPECT_TEST_PACKAGES_PATH = join(APPINSPECT_TEST_PATH, "python_analyzer_packages", "ast_searcher")

DUMMY_CHECK = 'check_dummy'

def _node_filter(node, ast_info):
    return node.func.attr.startswith('rea')


class TestAstSearcher(object):
    def setup_method(self, method):
        self.searcher = self._get_searcher_with_packages('file_access')

    def test_search_function_usages_by_tags(self):
        functions = metadata_store.query().tags([metadata_consts.TagConsts.FILE_READ_AND_WRITE]).functions()
        files_with_function_usages = self.searcher.search(functions, check_name=DUMMY_CHECK)
        assert_that(files_with_function_usages, not_none())
        value = files_with_function_usages['file_access.py']

        assert_that(value, not_none())
        assert_that(value['io.FileIO.read'][0]['line_number'], equal_to(2))

    def test_search_non_existing_function_usages(self):
        functions = metadata_store.query().tags([metadata_consts.TagConsts.MEMORY_MAPPING]).functions()
        files_with_function_usages = self.searcher.search(functions, check_name=DUMMY_CHECK)
        assert_that(files_with_function_usages, not_none())

    def test_search_node_filter(self):
        searcher = self._get_searcher_with_packages('filter_function')
        functions = metadata_store.query().tags([metadata_consts.TagConsts.FILE_READ_AND_WRITE]).functions()
        files_with_function_usages = searcher.search(functions, _node_filter, check_name=DUMMY_CHECK)
        assert_that(files_with_function_usages, not_none())
        value = files_with_function_usages['__init__.py']
        assert_that(value, not_none())
        assert_that(value['io.BytesIO.read'][0]['line_number'], equal_to(5))
        assert_that('io.FileIO.write' not in value)

    def test_search_usage_in_real_check(self):
        searcher = self._get_searcher_with_packages('search_usage_in_real_check')
        functions = metadata_store.query().name('kill').functions()

        def check_simple_demo():
            # check name is not given here
            files_with_function_usages = searcher.search(functions)
            assert_that(files_with_function_usages, not_none())
            value = files_with_function_usages['check.py']
            assert_that(value, not_none())
            assert_that(value['os.kill'][0]['line_number'], equal_to(3))

        check_simple_demo()


    def test_search_usage_in_real_check_with_trustedlib(self):
        pkg_path = join(APPINSPECT_TEST_PACKAGES_PATH, 'search_usage_in_real_check_with_trustedlib')
        test_file = join(pkg_path, 'check.py')
        hash_value = get_hash_file(open(test_file, 'rb').read())

        client = Client(files_folder=pkg_path)
        # add check.py to trustedlib
        client.trusted_libs.libs_data.get_trusted_check_and_libs().add(('check_simple_demo', hash_value))
        searcher = AstSearcher(client)

        functions = metadata_store.query().name('kill').functions()

        def check_simple_demo():
            files_with_function_usages = searcher.search(functions)
            assert_that(files_with_function_usages, not_none())
            assert_that('check.py' not in files_with_function_usages)
            assert_that('check_fake.py' in files_with_function_usages)

            check = files_with_function_usages['check_fake.py']
            assert_that(check, not_none())
            assert_that(check['os.kill'][0]['line_number'], equal_to(4))

        check_simple_demo()


    def _get_searcher_with_packages(self, package_path):
        fixed_load_pkg_path = join(APPINSPECT_TEST_PACKAGES_PATH, package_path)
        client = Client(files_folder=fixed_load_pkg_path)
        return AstSearcher(client)
