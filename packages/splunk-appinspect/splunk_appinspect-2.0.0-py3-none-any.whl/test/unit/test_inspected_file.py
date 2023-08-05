import os
from splunk_appinspect import inspected_file

def test_inspected_file():
	target_urls = ['https://firsturl.com', 'https://secondurl.com', 'https://thirdurl.com']
	data_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'data', 'inspected_file.txt')
	
	file_to_inspect = inspected_file.InspectedFile.factory(data_path)
	found_matches = file_to_inspect.search_for_patterns(['https://[\\w.-]*'])
	lines = set([int(path.split(':')[-1]) for path, match in found_matches])
	urls = [match.group() for path, match in found_matches]

	assert lines == set([1])
	assert sorted(urls) == sorted(target_urls)

