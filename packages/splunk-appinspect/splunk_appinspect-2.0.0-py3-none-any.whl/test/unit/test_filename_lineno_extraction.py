from splunk_appinspect import reporter

def test_filename_lineno_extraction():
    testcases = (
        ('file: README, line: 1', 'README', '1'),
        ('File: README, Line: 1', 'README', '1'),
        ('please invistage this file /package/README. File: README, Line: 1', 'README', '1'),
        ('File:default/app.conf, Line:1', 'default/app.conf', '1'),
        ('File: default/app.conf, Line: 1', 'default/app.conf', '1'),
        ('File: default/app.conf, Line number: 1.', 'default/app.conf', '1'),
        ('File: default/app.conf  Line: 1.', 'default/app.conf', '1'),
        ('File: default/app.conf; Line: 1.', 'default/app.conf', '1'),
        ('File: default/app.conf, Stanza: [install], Line: 1.', 'default/app.conf', '1'),
        ('Documentation will be read during code review.', '', ''),
        ('Please check the script. File: bin/test.py ', 'bin/test.py', ''),
        ('Line: 1', '', '1'),
    )
    for message, expect_filename, expect_lineno in testcases:
        filename, lineno = reporter.extract_filename_lineno(message)
        assert filename == expect_filename and lineno == expect_lineno