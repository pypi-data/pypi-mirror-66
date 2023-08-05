import bs4


class xml_node(object):
    def __init__(self, name):
        self.name = name


def find_xml_nodes_usages(xml_files, nodes):
    #  Outputs not_applicable if no xml files found
    findings = []
    for relative_filepath, full_filepath in xml_files:
        soup = bs4.BeautifulSoup(open(full_filepath, "rb"), "lxml-xml")
        for node in nodes:
            if hasattr(node, 'attrs'):
                findings_per_file = soup.find_all(node.name, attrs=node.attrs)
            else:
                findings_per_file = soup.find_all(node.name)
            findings_per_file = map(lambda e: (e, relative_filepath), findings_per_file)
            findings += findings_per_file
    return findings