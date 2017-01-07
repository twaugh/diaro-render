"""
Read Diaro data format
"""

from xml.etree import ElementTree as ET
from collections import namedtuple
import logging


DIARO_FOLDER_PROPS = ['title', 'color', 'pattern']
DiaroFolder = namedtuple('DiaroFolder', DIARO_FOLDER_PROPS)

DIARO_LOCATION_PROPS = ['title', 'address', 'lat', 'lng', 'zoom']
DiaroLocation = namedtuple('DiaroLocation', DIARO_LOCATION_PROPS)


class Diaro(object):
    def __init__(self, filename):
        self.folders = {}  # uid -> DiaroFolder
        self.locations = {}  # uid -> DiaroLocation

        root = ET.parse(filename).getroot()
        self._parse_root(root)

    def _gather_properties(self, node, properties_without_uid):
        properties = {
            'uid': None,
        }

        for prop in properties_without_uid:
            properties[prop] = None

        for prop in node:
            if properties[prop.tag] is None:
                properties[prop.tag] = prop.text or ''
            else:
                logging.warning("property %s defined twice for node %s",
                                node.tag)

        return properties

    def _parse_folders(self, folders):
        for folder in folders:
            assert folder.tag == 'r'
            properties = self._gather_properties(folder, DIARO_FOLDER_PROPS)
            if None in properties.values():
                logging.error("incomplete property list for folder %s",
                              properties.get('uid', '(?)'))
            else:
                uid = properties.pop('uid')
                diaro_folder = DiaroFolder(**properties)
                self.folders[uid] = diaro_folder
                logging.info("folder: %s", uid)

    def _parse_locations(self, locations):
        for location in locations:
            assert location.tag == 'r'
            properties = self._gather_properties(location, DIARO_LOCATION_PROPS)
            if None in properties.values():
                logging.error("incomplete property list for location %s",
                              properties.get('uid', '(?)'))
                logging.error("properties: %r", properties)
            else:
                uid = properties.pop('uid')
                diaro_location = DiaroLocation(**properties)
                self.locations[uid] = diaro_location
                logging.info("location: %s", uid)

    def _parse_root(self, root):
        assert root.tag == 'data'
        assert root.attrib['version'] == '2'

        for child in root:
            if child.tag == 'table':
                name = child.attrib['name']
                if name == 'diaro_folders':
                    self._parse_folders(child)
                elif name == 'diaro_locations':
                    self._parse_locations(child)
                else:
                    raise NotImplementedError
            else:
                raise NotImplementedError
