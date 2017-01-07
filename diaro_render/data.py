"""
Read Diaro data format
"""

from xml.etree import ElementTree as ET
from collections import namedtuple


DiaroFolder = namedtuple('DiaroFolder', ['title', 'color', 'pattern'])


class Diaro(object):
    def __init__(self, filename):
        self.folders = {}  # uid -> DiaroFolder

        root = ET.parse(filename).getroot()
        assert root.tag == 'data'
        assert root.attrib['version'] == '2'
