import splunk_appinspect.configuration_parser
import splunk_appinspect.splunk.util
import distutils.util
import unittest
from splunk_appinspect.splunk import TargetSplunkVersion


class ExampleTest(unittest.TestCase):

    def test_boolean_util(self):
        test_conf_str_common = """
            [A]
            acceleration = true

            [B]
            acceleration = no

            [C]
            acceleration = on

            [D]
            acceleration = 

        """
        tests = test_conf_str_common.split('\n')
        expected_common = [('true', 1),
                           ('no', 0),
                           ('on', 1),
                           ('', '')]
        # before fix: we use distutils.util.strtobool to get boolean value
        # it cannot handle values in ['', None]
        # so for the expected ('', ''), it will raise 'invalid truth value'
        with self.assertRaises(Exception): [(row[1][1], distutils.util.strtobool(row[1][1]))
                                            for row
                                            in splunk_appinspect.configuration_parser.configuration_lexer(tests)
                                            if row[0] == 'KEYVAL']
        # after fix: it will assert True
        results_common_after_fix = [(row[1][1], splunk_appinspect.splunk.util.normalizeBoolean(row[1][1]))
                                    for row
                                    in splunk_appinspect.configuration_parser.configuration_lexer(tests)
                                    if row[0] == 'KEYVAL']
        assert expected_common == results_common_after_fix

    def test_target_splunk_version(self):
        target_splunk_version = TargetSplunkVersion([])
        assert target_splunk_version >= "splunk_6_0"
        assert not target_splunk_version <= "splunk_8_0"  # Test a non-existed version.

        target_splunk_version = TargetSplunkVersion(['splunk_6_0'])
        assert target_splunk_version >= "splunk_6_0"
        assert not target_splunk_version >= "splunk_7_0"
        assert "splunk_5_0" <= target_splunk_version < 'splunk_7_0'

        target_splunk_version = TargetSplunkVersion(['splunk_6_0', 'splunk_6_1'])
        assert target_splunk_version >= "splunk_6_0"
        assert not target_splunk_version >= "splunk_7_0"
        assert "splunk_5_0" <= target_splunk_version < 'splunk_7_0'


if __name__ == '__main__':
    unittest.main()
