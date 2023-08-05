# Python Standard Libraries
import pytest
import re
import os

from splunk_appinspect.regex_matcher import RegexMatcher
from splunk_appinspect.regex_matcher import JSInsecureHttpRequestMatcher
from splunk_appinspect.regex_matcher import JSIFrameMatcher
from splunk_appinspect.regex_matcher import JSRemoteCodeExecutionMatcher
from splunk_appinspect.regex_matcher import JSConsoleLogMatcher
from splunk_appinspect.regex_matcher import JSWeakEncryptionMatcher
from splunk_appinspect.regex_matcher import JSUDPCommunicationMatcher
from splunk_appinspect.regex_matcher import JSReflectedXSSMatcher
from splunk_appinspect.regex_matcher import ConfEndpointMatcher
from splunk_appinspect.regex_matcher import SecretDisclosureInAllFilesMatcher
from splunk_appinspect.regex_matcher import SecretDisclosureInNonPythonFilesMatcher
from splunk_appinspect.regex_matcher import RegexBundle

REGEX_MATCHER_TEST_APP_DIR = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'data', 'regex_matcher_test')

JAVASCRIPT_TEST_APP_DIR = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'data', 'javascript_test')
INSECURE_HTTP_REQUEST_TEST_APP_DIR = os.path.join(JAVASCRIPT_TEST_APP_DIR, "insecure_http_request")
REMOTE_CODE_EXECUTION_TEST_APP_DIR = os.path.join(JAVASCRIPT_TEST_APP_DIR, "remote_code_execution")

class TestRegexMatcher:

    def test_match_with_default_regex_option(self):

        matcher = RegexMatcher([RegexBundle("abc")])
        result = matcher.match("abc ABC Abc")

        assert len(result) == 1

        assert result[0] == "abc"

    def test_match_with_ignore_case_regex_option(self):

        matcher = RegexMatcher([RegexBundle("abc")])
        result = matcher.match("abc ABC Abc", regex_option=re.IGNORECASE)

        assert len(result) == 3

        assert result[0] == "ABC"
        assert result[1] == "Abc"
        assert result[2] == 'abc'

    def test_match_string_array_with_default_regex_option(self):

        matcher = RegexMatcher([RegexBundle("\w+")])
        result = matcher.match_string_array(["a e b", "", "e c"])

        assert len(result) == 5

        assert result[0] == (1, "a")
        assert result[1] == (1, "b")
        assert result[2] == (1, "e")

        assert result[3] == (3, "c")
        assert result[4] == (3, "e")

    def test_match_string_array_with_ignore_case_regex_option(self):

        matcher = RegexMatcher([RegexBundle("abc")])
        result = matcher.match_string_array(["abc ABC", "", "", " aBC"], regex_option=re.IGNORECASE)

        assert len(result) == 3

        assert result[0] == (1, "ABC")
        assert result[1] == (1, "abc")
        assert result[2] == (4, "aBC")

    def test_match_file_with_default_regex_option(self):

        matcher = RegexMatcher([RegexBundle("abc")])
        file_path = os.path.join(REGEX_MATCHER_TEST_APP_DIR, "simple_match_test_ACD-1813.js")
        result = matcher.match_file(file_path)

        assert len(result) == 2

        assert result[0] == (1, "abc")
        assert result[1] == (2, "abc")

    def test_match_file_with_ignore_case_regex_option(self):

        matcher = RegexMatcher([RegexBundle("abc")])
        file_path = os.path.join(REGEX_MATCHER_TEST_APP_DIR, "simple_match_test_ACD-1813.js")
        result = matcher.match_file(file_path, regex_option=re.IGNORECASE)

        assert len(result) == 3

        assert result[0] == (1, "ABC")
        assert result[1] == (1, "abc")
        assert result[2] == (2, "abc")

    def test_match_string_with_very_long_match_result(self):

        matcher = RegexMatcher([RegexBundle("([a-z]+).+?([0-9]+)")])
        string = "abcd" + (''.join(['E'] * RegexMatcher.MESSAGE_LIMIT)) + "1234"
        result = matcher.match(string)

        assert len(result) == 1
        assert result[0] == '...abcd...1234...'

        matcher = RegexMatcher([RegexBundle(".+")])
        string = ''.join(['a'] * (RegexMatcher.MESSAGE_LIMIT + 5))
        result = matcher.match(string)

        assert len(result) == 1
        assert result[0] == ''.join(['a'] * RegexMatcher.MESSAGE_LIMIT) + '...'

class TestJSInsecureHttpRequestMatcher:

    def test_match_insecure_ajax_get_request(self):

        matcher = JSInsecureHttpRequestMatcher()
        string = 'a.open ( "GET" , "Http://www.xxx-xxx.com", true)'
        result = matcher.match(string, regex_option=re.IGNORECASE)

        assert len(result) == 1
        assert result[0] == 'a.open ( "GET" , "Http://www.xxx-xxx.com", true)'

    def test_match_insecure_ajax_post_request(self):
        matcher = JSInsecureHttpRequestMatcher()
        string = 'a.open("POST","localhost:8000", false)'
        result = matcher.match(string, regex_option=re.IGNORECASE)

        assert len(result) == 1
        assert result[0] == 'a.open("POST","localhost:8000", false)'

    def test_match_insecure_node_http_get_request(self):

        matcher = JSInsecureHttpRequestMatcher()
        string = 'http.get("HTTP://www.xxx.com")'
        result = matcher.match(string, regex_option=re.IGNORECASE)

        assert len(result) == 1
        assert result[0] == 'http.get("HTTP://www.xxx.com")'

    def test_match_insecure_node_http_post_request(self):

        matcher = JSInsecureHttpRequestMatcher()
        string = 'http.post  ("HTTP://xxx.com:1234")'
        result = matcher.match(string, regex_option=re.IGNORECASE)

        assert len(result) == 1
        assert result[0] == 'http.post  ("HTTP://xxx.com:1234")'

    def test_match_insecure_node_axios_get_request(self):

        matcher = JSInsecureHttpRequestMatcher()
        string = 'axios.get("www.xxx__aaa.com")'
        result = matcher.match(string, regex_option=re.IGNORECASE)

        assert len(result) == 1
        assert result[0] == 'axios.get("www.xxx__aaa.com")'

    def test_match_insecure_node_axios_post_request(self):

        matcher = JSInsecureHttpRequestMatcher()
        string = 'axios.post(  "www.xxx.com"  )'
        result = matcher.match(string, regex_option=re.IGNORECASE)

        assert len(result) == 1
        assert result[0] == 'axios.post(  "www.xxx.com"  )'

    def test_match_insecure_node_request_get_request(self):

        matcher = JSInsecureHttpRequestMatcher()
        string = 'request.get("http://www.xxx.com")'
        result = matcher.match(string, regex_option=re.IGNORECASE)

        assert len(result) == 1
        assert result[0] == 'request.get("http://www.xxx.com")'

    def test_match_insecure_node_request_post_request(self):
        matcher = JSInsecureHttpRequestMatcher()
        string = 'request.post ( "http://www.xxx.com" )'
        result = matcher.match(string, regex_option=re.IGNORECASE)

        assert len(result) == 1
        assert result[0] == 'request.post ( "http://www.xxx.com" )'

    def test_match_insecure_node_superagent_get_request(self):

        matcher = JSInsecureHttpRequestMatcher()
        string = 'superagent.get("http://www.xxx.com")'
        result = matcher.match(string, regex_option=re.IGNORECASE)

        assert len(result) == 1
        assert result[0] == 'superagent.get("http://www.xxx.com")'

    def test_match_insecure_node_superagent_post_request(self):

        matcher = JSInsecureHttpRequestMatcher()
        string = 'superagent.post ( "http://www.xxx.com")'
        result = matcher.match(string, regex_option=re.IGNORECASE)

        assert len(result) == 1
        assert result[0] == 'superagent.post ( "http://www.xxx.com")'

    def test_match_insecure_node_fly_get_request(self):

        matcher = JSInsecureHttpRequestMatcher()
        string = 'fly.get("www.xxx.com")'
        result = matcher.match(string, regex_option=re.IGNORECASE)

        assert len(result) == 1
        assert result[0] == 'fly.get("www.xxx.com")'

    def test_match_insecure_node_fly_post_request(self):

        matcher = JSInsecureHttpRequestMatcher()
        string = 'fly.post ( "www.xxx.com")'
        result = matcher.match(string, regex_option=re.IGNORECASE)

        assert len(result) == 1
        assert result[0] == 'fly.post ( "www.xxx.com")'

    def test_match_insecure_node_got_get_request(self):
        matcher = JSInsecureHttpRequestMatcher()
        string = 'got.get   (  "www.xxx.com")'
        result = matcher.match(string, regex_option=re.IGNORECASE)

        assert len(result) == 1
        assert result[0] == 'got.get   (  "www.xxx.com")'

    def test_match_insecure_node_got_post_request(self):
        matcher = JSInsecureHttpRequestMatcher()
        string = 'got.post ( "www.xxx.com" )'
        result = matcher.match(string, regex_option=re.IGNORECASE)

        assert len(result) == 1
        assert result[0] == 'got.post ( "www.xxx.com" )'

    def test_match_insecure_jquery_get_request(self):

        matcher = JSInsecureHttpRequestMatcher()
        string = '$.get ( "http://www.xxx.com" , function() { })'
        result = matcher.match(string, regex_option=re.IGNORECASE)

        assert len(result) == 1
        assert result[0] == '$.get ( "http://www.xxx.com" , function()'

        string = 'jQuery.get ( "http://www.xxx.com" , function() { })'
        result = matcher.match(string, regex_option=re.IGNORECASE)

        assert len(result) == 1
        assert result[0] == 'jQuery.get ( "http://www.xxx.com" , function()'

    def test_match_insecure_jquery_post_request(self):

        matcher = JSInsecureHttpRequestMatcher()
        string = '$.post( "www.xxx.com")'
        result = matcher.match(string, regex_option=re.IGNORECASE)

        assert len(result) == 1
        assert result[0] == '$.post( "www.xxx.com")'

        string = 'jQuery.post( "www.xxx.com")'
        result = matcher.match(string, regex_option=re.IGNORECASE)

        assert len(result) == 1
        assert result[0] == 'jQuery.post( "www.xxx.com")'

    def test_match_insecure_jquery_get_json_request(self):

        matcher = JSInsecureHttpRequestMatcher()
        string = '$.getJSON("www.xxx.com")'
        result = matcher.match(string, regex_option=re.IGNORECASE)

        assert len(result) == 1
        assert result[0] == '$.getJSON("www.xxx.com")'

        string = 'jQuery.getJSON("www.xxx.com")'
        result = matcher.match(string, regex_option=re.IGNORECASE)

        assert len(result) == 1
        assert result[0] == 'jQuery.getJSON("www.xxx.com")'

    def test_match_insecure_jquery_get_script_request(self):

        matcher = JSInsecureHttpRequestMatcher()
        string = '$.getScript("www.xxx.com")'
        result = matcher.match(string, regex_option=re.IGNORECASE)

        assert len(result) == 1
        assert result[0] == '$.getScript("www.xxx.com")'

        string = 'jQuery.getScript("www.xxx.com")'
        result = matcher.match(string, regex_option=re.IGNORECASE)

        assert len(result) == 1
        assert result[0] == 'jQuery.getScript("www.xxx.com")'

    def test_match_insecure_jquery_ajax_script_request(self):

        matcher = JSInsecureHttpRequestMatcher()
        string = '$.ajax({url = "www.xxx.com"})'
        result = matcher.match(string, regex_option=re.IGNORECASE)

        assert len(result) == 1
        assert result[0] == '$.ajax('

        string = 'jQuery.ajax({url = "www.xxx.com"})'
        result = matcher.match(string, regex_option=re.IGNORECASE)

        assert len(result) == 1
        assert result[0] == 'jQuery.ajax('

    def test_match_insecure_request_in_string_array(self):

        string_array = [
            'http.get("www.xxx.com")    $.post("www.xxx.com")',
            '', '',
            'axios.post("https://www.xxx.com")  $.get("www.xx.com")',
            '$.ajax({})',
            '  jQuery.ajax (']
        matcher = JSInsecureHttpRequestMatcher()
        result = matcher.match_string_array(string_array, regex_option=re.IGNORECASE)

        assert len(result) == 5

        assert result[0] == (1, '$.post("www.xxx.com")')
        assert result[1] == (1, 'http.get("www.xxx.com")')
        assert result[2] == (4, '$.get("www.xx.com")')
        assert result[3] == (5, '$.ajax(')
        assert result[4] == (6, 'jQuery.ajax (')

    def test_match_insecure_request_with_file_not_found(self):

        matcher = JSInsecureHttpRequestMatcher()
        file_path = os.path.join(INSECURE_HTTP_REQUEST_TEST_APP_DIR, "test.js")

        result = matcher.match_file(file_path, regex_option=re.IGNORECASE)
        assert len(result) == 0

    def test_match_insecure_request_with_simple_test_file(self):

        matcher = JSInsecureHttpRequestMatcher()
        file_path = os.path.join(INSECURE_HTTP_REQUEST_TEST_APP_DIR, 'simple_js_insecure_http_request_match_test_ACD-1813.js')

        result = matcher.match_file(file_path, regex_option=re.IGNORECASE)
        assert len(result) == 8

        assert result[0] == (1, '$.get("https:www.xxx.com")')
        assert result[1] == (3, 'http.get("www.xxx.com")')
        assert result[2] == (3, 'request.get("xx.com")')
        assert result[3] == (6, 'a.open("GET" , "xxx.com" , true)')
        assert result[4] == (9, 'b.open("POST" , "xxx.com" , false)')
        assert result[5] == (11, '$.ajax(')
        assert result[6] == (16, 'jQuery.ajax (')
        assert result[7] == (22, '$.ajax')

    def test_match_insecure_request_with_real_safe_test_file(self):

        matcher = JSInsecureHttpRequestMatcher()
        file_path = os.path.join(INSECURE_HTTP_REQUEST_TEST_APP_DIR, 'safe_test_file_ACD-1813.js')

        result = matcher.match_file(file_path, re.IGNORECASE)
        assert len(result) == 0

    def test_match_insecure_request_with_real_unsafe_test_file(self):

        matcher = JSInsecureHttpRequestMatcher()
        file_path = os.path.join(INSECURE_HTTP_REQUEST_TEST_APP_DIR, 'unsafe_test_file_ACD-1813.js')

        result = matcher.match_file(file_path, re.IGNORECASE)

        assert len(result) == 7

        assert result[0] == (9255, 'jQuery.get( url, data, callback, "json" )')
        assert result[1] == (9259, 'jQuery.get( url, undefined, callback, "script" )')
        assert result[2] == (9274, 'jQuery.ajax(')
        assert result[3] == (9286, 'jQuery.ajax(')
        assert result[4] == (9889, 'jQuery.ajax(')
        assert result[5] == (84329, 'xhr.open(\'GET\', url, true)')
        assert result[6] == (84353, 'xhr.open(\'GET\', url, true)')

class TestJSIFrameMatcher:

    def test_match_iframe_use(self):
        matcher = JSIFrameMatcher()
        string = '<iframe src="somewebsite" witdth="100" height="100">'
        result = matcher.match(string, regex_option=re.IGNORECASE)
        assert len(result) == 1

    def test_match_iframe_use_with_single_quotes(self):
        matcher = JSIFrameMatcher()
        string = '<iframe src=\'somewebsite\' witdth=\'100\' height=\'100\'>'
        result = matcher.match(string, regex_option=re.IGNORECASE)
        assert len(result) == 1

    def test_match_iframe_use_with_multiple_lines(self):
        matcher = JSIFrameMatcher()
        string = '<iframe src="somewebsite" \n>'
        result = matcher.match(string, regex_option=re.IGNORECASE)
        assert len(result) == 1

    def test_match_iframe_use_without_src(self):
        matcher = JSIFrameMatcher()
        string = '<iframe witdth="100">'
        result = matcher.match(string, regex_option=re.IGNORECASE)
        assert len(result) == 0

    def test_match_iframe_use_with_nonexecutable_javascript(self):
        matcher = JSIFrameMatcher()
        string = '<iframe src="javascript:0">'
        result = matcher.match(string, regex_option=re.IGNORECASE)
        assert len(result) == 1

class TestConosleLogMather:

    def test_console_log_data_leakage_with_dom_dereference(self):
        matcher = JSConsoleLogMatcher()
        string = 'console.log(document.getElementById(password).value)'
        result = matcher.match(string, regex_option=re.IGNORECASE)
        assert len(result) == 1

    def test_console_log_data_leakage_with_jquery(self):
        matcher = JSConsoleLogMatcher()
        string = 'console.log($("#password").val())'
        result = matcher.match(string, regex_option=re.IGNORECASE)
        assert len(result) == 1

    def test_console_log_data_leakage_with_var(self):
        matcher = JSConsoleLogMatcher()
        string = 'console.log(password)'
        result = matcher.match(string, regex_option=re.IGNORECASE)
        assert len(result) == 1

    def test_console_log_with_password_outside(self):
        matcher = JSConsoleLogMatcher()
        string = 'console.log(); var password;'
        result = matcher.match(string, regex_option=re.IGNORECASE)
        assert len(result) == 0

class TestJSRemoteCodeExecutionMatcher:

    def test_match_global_eval_string_with_dollar(self):

        matcher = JSRemoteCodeExecutionMatcher()
        string = '$.globalEval(" var a = b;")'
        result = matcher.match(string)

        assert len(result) == 1
        assert result[0] == '$.globalEval(" var a = b;"'


    def test_match_global_eval_string_with_jquery(self):

        matcher = JSRemoteCodeExecutionMatcher()
        string = 'jQuery.globalEval(" var a = b;")'
        result = matcher.match(string)

        assert len(result) == 1
        assert result[0] == 'jQuery.globalEval(" var a = b;"'


    def test_match_eval_string(self):

        matcher = JSRemoteCodeExecutionMatcher()
        string = 'eval ( text )'
        result = matcher.match(string)

        assert len(result) == 1
        assert result[0] == 'eval ( text '


    def test_match_remote_code_execution_in_string_array(self):

        matcher = JSRemoteCodeExecutionMatcher()
        string_array = [
            '',
            'test.globalEval(" a = b")',
            '',
            ' eval(a , "" , func()',
        ]
        result = matcher.match_string_array(string_array)

        assert len(result) == 2

        assert result[0] == (2, 'test.globalEval(" a = b"')
        assert result[1] == (4, 'eval(a , "" , func(')


    def test_match_remote_code_execution_with_real_unsafe_file(self):

        matcher = JSRemoteCodeExecutionMatcher()
        file_path = os.path.join(REMOTE_CODE_EXECUTION_TEST_APP_DIR, 'test_file_with_possible_remote_code_execution_ACD-2013.js')

        result = matcher.match_file(file_path)

        assert len(result) == 1

        assert result[0] == (25074, 'jQuery.globalEval( text ')


    def test_match_remote_code_execution_with_real_safe_file(self):

        matcher = JSRemoteCodeExecutionMatcher()
        file_path = os.path.join(REMOTE_CODE_EXECUTION_TEST_APP_DIR, 'test_file_without_possible_remote_code_execution_ACD-2013.js')

        result = matcher.match_file(file_path)

        assert len(result) == 0


class TestWeakEncryption:

    def test_weak_encryption_with_spaces(self):
        matcher = JSWeakEncryptionMatcher()
        string = 'CryptoJS . DES.encrypt(message, keyHex, { iv:ivHex, mode: CryptoJS.mode.CBC, padding:CryptoJS.pad.Pkcs7}'
        result = matcher.match(string, regex_option=re.IGNORECASE)
        assert len(result) == 1

    def test_digest_algorithm(self):
        matcher = JSWeakEncryptionMatcher()
        string = 'CryptoJS . MD5'
        result = matcher.match(string, regex_option=re.IGNORECASE)
        assert len(result) == 1

        string = 'CryptoJS . sha1'
        result = matcher.match(string, regex_option=re.IGNORECASE)
        assert len(result) == 1

    def test_weak_encryption_with_lower_case(self):
        matcher = JSWeakEncryptionMatcher()
        string = 'cryptojs.sha1'
        result = matcher.match(string, regex_option=re.IGNORECASE)
        assert len(result) == 1


class TestUDPCommunication:

    def test_media_stream_interface(self):
        matcher = JSUDPCommunicationMatcher()
        string = 'navigator.mediaDevices.getUserMedia'
        result = matcher.match(string, regex_option=re.IGNORECASE)
        assert len(result) == 1

    def test_peer_connection_interface(self):
        matcher = JSUDPCommunicationMatcher()
        string = 'pc1 = new RTCPeerConnection(servers);'
        result = matcher.match(string, regex_option=re.IGNORECASE)
        assert len(result) == 1

    def test_udp_socket_interface(self):
        matcher = JSUDPCommunicationMatcher()
        string = 'var step1 = vendor.createUdpSocket(options);'
        result = matcher.match(string, regex_option=re.IGNORECASE)
        assert len(result) == 1

        string = 'var socket = chrome.sockets.udp'
        result = matcher.match(string, regex_option=re.IGNORECASE)
        assert len(result) == 1

class TestReflectedXSSMatcher:

    def test_image_tag_with_src(self):
        matcher = JSReflectedXSSMatcher()
        string = '<img src  =  "javascript:alert(\"sfd\"">'
        result = matcher.match(string, regex_option=re.IGNORECASE)
        assert len(result) == 1

    def test_image_tag_with_src_and_without_javascript(self):
        matcher = JSReflectedXSSMatcher()
        string = '<img src = "javascript:0">'
        result = matcher.match(string, regex_option=re.IGNORECASE)
        assert len(result) == 0

        string = '<img src = "javascript:false">'
        result = matcher.match(string, regex_option=re.IGNORECASE)
        assert len(result) == 0

    def test_image_tag_with_dynsrc(self):
        matcher = JSReflectedXSSMatcher()
        string = '<img dynsrc="javascript:alert">'
        result = matcher.match(string, regex_option=re.IGNORECASE)
        assert len(result) == 1

    def test_image_tag_with_lowsrc(self):
        matcher = JSReflectedXSSMatcher()
        string = '<img lowsrc="javascript:alert">'
        result = matcher.match(string, regex_option=re.IGNORECASE)
        assert len(result) == 1

    def test_bgsound_with_src(self):
        matcher = JSReflectedXSSMatcher()
        string = '<bgsound src ="javascript:alert">'
        result = matcher.match(string, regex_option=re.IGNORECASE)
        assert len(result) == 1

    def test_frame_with_src(self):
        matcher = JSReflectedXSSMatcher()
        string = '<frame src = "javascript:alert">'
        result = matcher.match(string, regex_option=re.IGNORECASE)
        assert len(result) == 1

    def test_iframe_with_src(self):
        matcher = JSReflectedXSSMatcher()
        string = '<iframe src = "javascript:alert">'
        result = matcher.match(string, regex_option=re.IGNORECASE)
        assert len(result) == 1

    def test_a_with_onmouseover(self):
        matcher = JSReflectedXSSMatcher()
        string = '<a onmouseover="">'
        result = matcher.match(string, regex_option=re.IGNORECASE)
        assert len(result) == 1

    def test_image_with_onmouseover(self):
        matcher = JSReflectedXSSMatcher()
        string = '<img onmouseover = "">'
        result = matcher.match(string, regex_option=re.IGNORECASE)
        assert len(result) == 1

    def test_src_is_sharp_with_onmouseover(self):
        matcher = JSReflectedXSSMatcher()
        string = '<img src = # onmouseover = "alert">'
        result = matcher.match(string, regex_option=re.IGNORECASE)
        assert len(result) == 1

    def test_src_is_empty_with_onmouseover(self):
        matcher = JSReflectedXSSMatcher()
        string = '<img src= onmouseover = "alert">'
        result = matcher.match(string, regex_option=re.IGNORECASE)
        assert len(result) == 1

    def test_src_is_slash_with_onmouseover(self):
        matcher = JSReflectedXSSMatcher()
        string = '<img src = / onerror = "alert">'
        result = matcher.match(string, regex_option=re.IGNORECASE)
        assert len(result) == 1

    def test_input_type_is_image_with_src(self):
        matcher = JSReflectedXSSMatcher()
        string = '<input type = "image" src = "javascript:alert()">'
        result = matcher.match(string, regex_option=re.IGNORECASE)
        assert len(result) == 1

    def test_body_table_td_with_background_attribute(self):
        matcher = JSReflectedXSSMatcher()
        string = '<body background = "javascript:alert">'
        result = matcher.match(string, regex_option=re.IGNORECASE)
        assert len(result) == 1

        string = '<table background = "javascript:alert">'
        result = matcher.match(string, regex_option=re.IGNORECASE)
        assert len(result) == 1

        string = '<td background = "javascript:alert">'
        result = matcher.match(string, regex_option=re.IGNORECASE)
        assert len(result) == 1

    def test_svg_and_body_with_onload_attribute(self):
        matcher = JSReflectedXSSMatcher()
        string = '<svg onload = "alert">'
        result = matcher.match(string, regex_option=re.IGNORECASE)
        assert len(result) == 1

        string = '<body onload  =  "alert">'
        result = matcher.match(string, regex_option=re.IGNORECASE)
        assert len(result) == 1

    def test_br_with_size_attribute(self):
        matcher = JSReflectedXSSMatcher()
        string = '<br size = "&{alert}">'
        result = matcher.match(string, regex_option=re.IGNORECASE)
        assert len(result) == 1

    def test_link_with_href(self):
        matcher = JSReflectedXSSMatcher()
        string = '<link href = "javascript:alert">'
        result = matcher.match(string, regex_option=re.IGNORECASE)
        assert len(result) == 1

    def test_div_with_background_image_in_style(self):
        matcher = JSReflectedXSSMatcher()
        string = '<div style = "background-image:url(javascript:alert)>'
        result = matcher.match(string, regex_option=re.IGNORECASE)
        assert len(result) == 1

    def test_match_form_get_without_assignation(self):
        matcher = JSReflectedXSSMatcher()
        string = "form.element.test_id"
        result = matcher.match(string)
        assert len(result) == 0


class TestConfEndpointMatcher:

    matcher = ConfEndpointMatcher()

    def test_serviceNS_endpoint(self):
        string = "http://127.0.0.1:8000/en-US/splunkd/__raw/servicesNS/admin/" \
                 "stored_xss/configs/conf-savedsearches/Web%20Search?output_mode=json"
        result = self.matcher.match(string)
        assert len(result) == 1

    def test_service_endpoint(self):
        string = "https://<host>:<mPort>/services/configs/conf-{file}/{stanza}"
        result = self.matcher.match(string)
        assert len(result) == 1

    def test_properties_endpoint(self):
        string = "https://<host>:<mPort>/services/properties/{file}/{stanza}/{key}"
        result = self.matcher.match(string)
        assert len(result) == 1


class TestSecretDisclosureInAllFilesMatcher:

    matcher = SecretDisclosureInAllFilesMatcher()

    def test_huge_json_file(self):
        '''
        If this test case is stuck, if means we have perf-issue
        '''
        result = self.matcher.match_file(filepath=os.path.join(REGEX_MATCHER_TEST_APP_DIR, 'canned_response_kpi.json'))
        assert result == []

    def test_rsa_private_key(self):

        string = 'haha-----BEGIN RSA PRIVATE KEY-----haha'
        result = self.matcher.match(string)
        assert result == ['-----BEGIN RSA PRIVATE KEY-----']

    def test_openssh_private_key(self):

        string = '-----BEGIN OPENSSH PRIVATE KEY-----'
        result = self.matcher.match(string)
        assert result == ['-----BEGIN OPENSSH PRIVATE KEY-----']

    def test_dsa_private_key(self):

        string = '-----BEGIN DSA PRIVATE KEY-----'
        result = self.matcher.match(string)
        assert result == ['-----BEGIN DSA PRIVATE KEY-----']

    def test_es_private_key(self):

        string = '-----BEGIN EC PRIVATE KEY-----'
        result = self.matcher.match(string)
        assert result == ['-----BEGIN EC PRIVATE KEY-----']

    def test_pgp_private_key(self):

        string = '-----BEGIN PGP PRIVATE KEY BLOCK-----'
        result = self.matcher.match(string)
        assert result == ['-----BEGIN PGP PRIVATE KEY BLOCK-----']

    def test_secret_in_url(self):

        string = 'https://www.abc.com?token=helloworld'
        result = self.matcher.match(string)
        assert len(result) == 1

    def test_secret_in_subdomain_url(self):

        string = 'http://www.abc.com/haha/token=fortest'
        result = self.matcher.match(string)
        assert len(result) == 1

    def test_aws_key(self):

        string = 'AKIAABCDEFGHIJKLMN12'
        result = self.matcher.match(string)
        assert len(result) == 1

        string = 'AKIAABCDEFGHIJKLMN_23'
        result = self.matcher.match(string)
        assert len(result) == 0

    def test_github_token(self):

        string = 'github  = "{}"'.format(''.join(['a'] * 40))
        result = self.matcher.match(string)
        assert len(result) == 1

        string = 'github="{}"'.format(''.join(['b'] * 41))
        result = self.matcher.match(string)
        assert len(result) == 0


    def test_slack_token(self):

        number_string = ''.join(['0'] * 12)
        mix_string = ''.join(['a0'] * 16)
        string = 'xoxa-{}-{}-{}-{}'.format(number_string, number_string, number_string, mix_string)
        result = self.matcher.match(string)
        assert len(result) == 1


class TestSecretDisclosureInNonPythonFilesMatcher:

    matcher = SecretDisclosureInNonPythonFilesMatcher()

    def test_password_disclosure(self):

        string = 'password=hahaha'
        result = self.matcher.match(string)
        assert len(result) == 1

        string = 'passwd = sfsdaf'
        result = self.matcher.match(string)
        assert len(result) == 1

        string = 'privpass= sdfdsf'
        result = self.matcher.match(string)
        assert len(result) == 1

    def test_apikey(self):

        result = self.matcher.match_file(filepath=os.path.join(REGEX_MATCHER_TEST_APP_DIR, "api_key_usage.conf"))
        assert len(result) == 1

    def test_filepath_affect_regex_generation(self):

        # same content, different filepath, use different regex
        result = self.matcher.match_file(os.path.abspath(os.path.join(REGEX_MATCHER_TEST_APP_DIR, "check_for_secret_disclosure", 'pkg1', "default", "props.conf")))
        assert len(result) == 1
        assert result[0] == (1, "SEDCMD-jenkins-unencrypted_password = haha")

        result = self.matcher.match_file(os.path.abspath(os.path.join(REGEX_MATCHER_TEST_APP_DIR, "check_for_secret_disclosure", 'pkg2', "default", "props_bk.conf")))
        assert len(result) == 1
        assert result[0] == (1, "D-jenkins-unencrypted_password = haha")

    def test_filepath_affect_result_generation(self):

        result = self.matcher.match_file(os.path.join(REGEX_MATCHER_TEST_APP_DIR, "check_for_secret_disclosure", "pkg3", "default", "props.conf"))
        assert len(result) == 1
        assert result[0] == (1, "haha_password = hahahahahahahahahahahahahahahahahahahahahahahahahahahahahahahahahahahahahahahahahahahahahahahahahahahahahahahaha")

        result = self.matcher.match_file(os.path.join(REGEX_MATCHER_TEST_APP_DIR, "check_for_secret_disclosure", "pkg4", "default", "props_bk.conf"))
        assert len(result) == 1
        assert result[0] == (1, '...password...')