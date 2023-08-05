from splunk_appinspect.configuration_file import ConfigurationFile
from splunk_appinspect.app_util import AppVersionNumberMatcher
from splunk_appinspect import configuration_parser


mock_conf = """
# The following configuration reads all the files in the directory /var/log.

[monitor:///var/log/httpd]
sourcetype = access_common
ignoreOlderThan = 7d

[monitor:///mnt/logs]
host_segment = 3

[tcp://:9997]

[tcp://:9995]
connection_host = dns
sourcetype = log4j
source = tcp:9995

[tcp://10.1.1.10:9995]
host = webhead-1
sourcetype = access_common
source = //10.1.1.10/var/log/apache/access.log

[splunktcp://:9996]
connection_host = dns

[splunktcp://10.1.1.100:9996]

[tcp://syslog.corp.company.net:514]
sourcetype = syslog
connection_host = dns

[splunktcptoken://tok1]
token = $1$ifQTPTzHD/BA8VgKvVcgO1KQAtr3N1C8S/1uK3nAKIE9dd9e9g==

# Set up Secure Sockets Layer (SSL):

[SSL]
serverCert=$SPLUNK_HOME/etc/auth/server.pem
password=password
rootCA=$SPLUNK_HOME/etc/auth/cacert.pem
requireClientCert=false

[splunktcp-ssl:9996]

[stanza1]
key1 = v1 v2 v3
 key2 = v1 v2v3 v4
key3 key4 = v1
* Splunk cannot read the modular name unless a parameter is specified. 
  Therefore, ITSI passes 'owner = <string>'.
"""


def test_build_lookup_with_empty_config():
    cf = ConfigurationFile()
    lookup = cf.build_lookup()
    assert len(lookup) == 0


def test_build_lookup_with_config():
    expected_result = {
        'splunktcp-ssl:9996': [],
        'monitor:///mnt/logs': ['host_segment'],
        'SSL': ['serverCert', 'password', 'rootCA', 'requireClientCert'],
        'monitor:///var/log/httpd': ['ignoreOlderThan', 'sourcetype'],
        'splunktcp://10.1.1.100:9996': [],
        'tcp://10.1.1.10:9995': ['source', 'host', 'sourcetype'],
        'tcp://syslog.corp.company.net:514': ['connection_host', 'sourcetype'],
        'splunktcp://:9996': ['connection_host'],
        'tcp://:9995': ['source', 'connection_host', 'sourcetype'],
        'splunktcptoken://tok1': ['token'],
        'tcp://:9997': [],
        'stanza1': ['key1', 'key2']
    }
    cf = ConfigurationFile()
    configuration_parser.parse(mock_conf, cf, configuration_parser.configuration_lexer)
    lookup = cf.build_lookup()

    for key in lookup:
        assert key in expected_result
        assert sorted(lookup[key]) == sorted(expected_result[key])


def test_build_lookup_with_config_wrong_result():
    unexpected_result = {
        'splunktcp-ssl:9997': [],
        'monitor:///mnt/logs': ['host_segment'],
        'SSL': ['serverCert', 'password', 'root', 'requireClientCert'],
        'monitor:///var/log/httpd': ['ignoreOlderThan', 'sourcetype', 'cats'],
        'splunktcp://10.1.1.100:9996': [],
        'tcp://10.1.1.10:9995': ['source', 'host', 'sourcetype'],
        'tcp://syslog.corp.company.net:514': ['connection_host', 'sourcetype'],
        'splunktcp://:9996': ['connection_host', 'dog'],
        'tcp://:9995': ['source', 'connection_host', 'sourcetype'],
        'splunktcptoken://tok1': ['token'],
        'tcp://:9997': [],
        'noodles': [],
    }
    cf = ConfigurationFile()
    configuration_parser.parse(mock_conf, cf, configuration_parser.configuration_lexer)
    lookup = cf.build_lookup()
    assert lookup != unexpected_result

def test_config_lineno_parsing():
    expected_result = [
        ('STANZA', 'monitor:///var/log/httpd', 4),
        ('KEYVAL', ('sourcetype', 'access_common'), 5),
        ('KEYVAL', ('ignoreOlderThan', '7d'), 6),
        ('STANZA', 'monitor:///mnt/logs', 8),
        ('KEYVAL', ('host_segment', '3'), 9),
        ('STANZA', 'tcp://:9997', 11),
        ('STANZA', 'tcp://:9995', 13),
        ('KEYVAL', ('connection_host', 'dns'), 14),
        ('KEYVAL', ('sourcetype', 'log4j'), 15),
        ('KEYVAL', ('source', 'tcp:9995'), 16),
        ('STANZA', 'tcp://10.1.1.10:9995', 18),
        ('KEYVAL', ('host', 'webhead-1'), 19),
        ('KEYVAL', ('sourcetype', 'access_common'), 20),
        ('KEYVAL', ('source', '//10.1.1.10/var/log/apache/access.log'), 21),
        ('STANZA', 'splunktcp://:9996', 23),
        ('KEYVAL', ('connection_host', 'dns'), 24),
        ('STANZA', 'splunktcp://10.1.1.100:9996', 26),
        ('STANZA', 'tcp://syslog.corp.company.net:514', 28),
        ('KEYVAL', ('sourcetype', 'syslog'), 29),
        ('KEYVAL', ('connection_host', 'dns'), 30),
        ('STANZA', 'splunktcptoken://tok1', 32),
        ('KEYVAL', ('token', '$1$ifQTPTzHD/BA8VgKvVcgO1KQAtr3N1C8S/1uK3nAKIE9dd9e9g=='), 33),
        ('STANZA', 'SSL', 37),
        ('KEYVAL', ('serverCert', '$SPLUNK_HOME/etc/auth/server.pem'), 38),
        ('KEYVAL', ('password', 'password'), 39),
        ('KEYVAL', ('rootCA', '$SPLUNK_HOME/etc/auth/cacert.pem'), 40),
        ('KEYVAL', ('requireClientCert', 'false'), 41),
        ('STANZA', 'splunktcp-ssl:9996', 43),
        ('STANZA', 'stanza1', 45),
        ('KEYVAL', ('key1', 'v1 v2 v3'), 46),
        ('KEYVAL', ('key2', 'v1 v2v3 v4'), 47),
        ('RANDSTRING', 'key3 key4 = v1', 48),
    ]
    cf = ConfigurationFile()
    configuration_parser.parse(mock_conf, cf, configuration_parser.configuration_lexer)
    current_section = None
    for result in expected_result:
        if result[0] == 'STANZA':
            current_section = cf.get_section(result[1])
            assert current_section.lineno == result[2]
        elif result[0] == 'KEYVAL':
            assert current_section is not None, 'Unexpected KEYVAL with no section'
            assert current_section.get_option(result[1][0]).lineno == result[2]


class TestAppVersionNumberMatcher(object):
    matcher = AppVersionNumberMatcher()

    def test_good_version_number_release(self):
        string = "1.0.2"
        result = self.matcher.match(string)
        assert len(result) == 2

    def test_good_version_number_pre_release(self):
        string = "1.0.2beta"
        result = self.matcher.match(string)
        assert len(result) == 2

    def test_good_version_number_pre_release_malformed(self):
        string = "1.0.2 Beta"
        result = self.matcher.match(string)
        assert len(result) == 0

    def test_version_number_major_only(self):
        string = "1"
        result = self.matcher.match(string)
        assert len(result) == 0

    def test_version_number_major_minor_only(self):
        string = "1.0"
        result = self.matcher.match(string)
        assert len(result) == 1

    def test_version_number_non_numeric(self):
        string = "whistlewhileyouwork"
        result = self.matcher.match(string)
        assert len(result) == 0

    def test_version_number_malformed(self):
        string = "1.2.3.4"
        result = self.matcher.match(string)
        assert len(result) == 0
