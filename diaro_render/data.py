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

DIARO_ATTACHMENT_PROPS = ['entry_uid', 'type', 'filename', 'position']
DiaroAttachment = namedtuple('DiaroAttachment', DIARO_ATTACHMENT_PROPS)

DIARO_ENTRY_PROPS = ['date', 'tz_offset', 'title', 'text',
                     'folder_uid', 'location_uid', 'tags',
                     'primary_photo_uid']
DiaroEntry = namedtuple('DiaroEntry', DIARO_ENTRY_PROPS)


class Diaro(object):
    def __init__(self, filename):
        self.folders = {}  # uid -> DiaroFolder
        self.locations = {}  # uid -> DiaroLocation
        self.attachments = {}  # uid -> DiaroAttachment
        self.entries = {}  # uid -> DiaroEntry

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
                logging.error("incomplete property list for folder: %r",
                              properties)
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
                logging.error("incomplete property list for location: %r",
                              properties)
            else:
                uid = properties.pop('uid')
                diaro_location = DiaroLocation(**properties)
                self.locations[uid] = diaro_location
                logging.info("location: %s", uid)

    def _parse_entries(self, entries):
        for entry in entries:
            assert entry.tag == 'r'
            properties = self._gather_properties(entry, DIARO_ENTRY_PROPS)
            if None in properties.values():
                logging.error("incomplete property list for entry: %r",
                              properties)
            else:
                uid = properties.pop('uid')
                diaro_entry = DiaroEntry(**properties)
                self.entries[uid] = diaro_entry
                logging.info("entry: %s", uid)

    def _parse_attachments(self, attachments):
        for attachment in attachments:
            assert attachment.tag == 'r'
            properties = self._gather_properties(attachment,
                                                 DIARO_ATTACHMENT_PROPS)
            if None in properties.values():
                logging.error("incomplete property list for attachment: %r",
                              properties)
            else:
                uid = properties.pop('uid')
                diaro_attachment = DiaroAttachment(**properties)
                self.attachments[uid] = diaro_attachment
                logging.info("attachment: %s", uid)

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
                elif name == 'diaro_entries':
                    self._parse_entries(child)
                elif name == 'diaro_attachments':
                    self._parse_attachments(child)
                else:
                    raise NotImplementedError
            else:
                raise NotImplementedError
