"""
Read Diaro data format

Copyright (C) 2017, 2019
Authors:
  Tim Waugh <tim@cyberelk.net>

This program is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 2 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program; if not, write to the Free Software
Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.
"""

from xml.etree import ElementTree as ET
from collections import namedtuple
import logging


DIARO_FOLDER_PROPS = ['uid', 'title', 'color', 'pattern']
DiaroFolder = namedtuple('DiaroFolder', DIARO_FOLDER_PROPS)

DIARO_LOCATION_PROPS = ['uid', 'title', 'address', 'lat', 'lng', 'zoom']
DiaroLocation = namedtuple('DiaroLocation', DIARO_LOCATION_PROPS)

DIARO_ATTACHMENT_PROPS = ['uid', 'entry_uid', 'type', 'filename', 'position']
DiaroAttachment = namedtuple('DiaroAttachment', DIARO_ATTACHMENT_PROPS)

DIARO_ENTRY_PROPS = ['uid', 'date', 'tz_offset', 'title', 'text',
                     'folder_uid', 'location_uid', 'tags',
                     'primary_photo_uid', 'weather_temperature',
                     'weather_icon', 'weather_description', 'mood']


class DiaroEntry(object):
    def __init__(self, **kwargs):
        assert all(kwarg in DIARO_ENTRY_PROPS for kwarg in kwargs)
        self.__dict__.update(kwargs)


class Diaro(object):
    def __init__(self, filename):
        self.folders = {}  # uid -> DiaroFolder
        self.locations = {}  # uid -> DiaroLocation
        self.attachments = {}  # uid -> DiaroAttachment
        self.entries = {}  # uid -> DiaroEntry

        root = ET.parse(filename).getroot()
        self._parse_root(root)

    def get_entries_for_folders(self, folder_uids):
        """
        Return entries in a given folders, in date order.
        """

        folder_uids = list(folder_uids)
        entries = [entry for entry in self.entries.values()
                   if entry.folder_uid in folder_uids]
        entries.sort(key=lambda x: x.date)
        return entries

    def get_attachments_for_entry(self, entry_uid):
        """
        Return attachments for a given entry in position order.
        """

        attachments = [attachment for attachment in self.attachments.values()
                       if attachment.entry_uid == entry_uid]
        attachments.sort(key=lambda x: x.position)
        return attachments

    def _gather_properties(self, node, properties):
        props = {}
        for prop in node:
            if prop.tag not in props:
                props[prop.tag] = prop.text or ''
            else:
                logging.warning("property %s defined twice for node %s",
                                node.tag)

        return props

    def _parse_folders(self, folders):
        for folder in folders:
            assert folder.tag == 'r'
            properties = self._gather_properties(folder, DIARO_FOLDER_PROPS)
            if None in properties.values():
                logging.error("incomplete property list for folder: %r",
                              properties)
            else:
                uid = properties['uid']
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
                uid = properties['uid']
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
                uid = properties['uid']
                properties['date'] = int(properties['date'])
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
                uid = properties['uid']
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
                elif name in ('diaro_templates', 'diaro_moods'):
                    continue
                else:
                    raise NotImplementedError
            else:
                raise NotImplementedError
