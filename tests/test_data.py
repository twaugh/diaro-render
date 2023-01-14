"""
Read Diaro data format - tests

Copyright (C) 2017
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

from diaro_render.data import Diaro
import pytest
from textwrap import dedent
from tempfile import NamedTemporaryFile


class TestDiaro(object):
    def test_empty_xml(self):
        xml = dedent("""\
            <data version="2">
            </data>
            """)

        with NamedTemporaryFile(mode='w') as fp:
            fp.write(xml)
            fp.flush()
            diaro = Diaro(filename=fp.name)

    def test_template(self):
        xml = dedent("""\
            <data version="2">
            <table name="diaro_templates">
            <r>
               <uid>73c5b749a50f0628667988147ca663c2</uid>
               <name>Template</name>
               <title>Title</title>
               <color>#000000</color>
               <text>text01</text>
            </r>
            </table>
            </data>
            """)

        with NamedTemporaryFile(mode='w') as fp:
            fp.write(xml)
            fp.flush()
            diaro = Diaro(filename=fp.name)

    def test_folder(self):
        xml = dedent("""\
            <data version="2">
            <table name="diaro_folders">
            <r>
               <uid>73c5b749a50f0628667988147ca663c2</uid>
               <title>Diary entries</title>
               <color>#000000</color>
               <pattern>pattern01</pattern>
            </r>
            </table>
            </data>
            """)

        with NamedTemporaryFile(mode='w') as fp:
            fp.write(xml)
            fp.flush()
            diaro = Diaro(filename=fp.name)

        assert len(diaro.folders) == 1
        assert '73c5b749a50f0628667988147ca663c2' in diaro.folders
        folder = diaro.folders['73c5b749a50f0628667988147ca663c2']
        assert folder.title == 'Diary entries'
        assert folder.color == '#000000'
        assert folder.pattern == 'pattern01'

    @pytest.mark.parametrize('folders', [
        [
            {
                'uid': '1',
                'title': 'title1',
                'color': '#111111',
                'pattern': 'patern01',
            },

            {
                'uid': '2',
                'title': 'title2',
                'color': '#222222',
                'pattern': 'pattern02',
            },
        ],
    ])
    def test_folders(self, folders):
        xml = dedent("""\
            <data version="2">
            <table name="diaro_folders">
            """)

        for folder in folders:
            xml += dedent("""\
                <r>
                  <uid>{uid}</uid>
                  <title>{title}</title>
                  <color>{color}</color>
                  <pattern>{pattern}</pattern>
                </r>
                """.format(**folder))

        xml += dedent("""\
            </table>
            </data>
            """)

        with NamedTemporaryFile(mode='w') as fp:
            fp.write(xml)
            fp.flush()
            diaro = Diaro(filename=fp.name)

        assert len(diaro.folders) == len(folders)

    def test_location(self):
        xml = dedent("""\
            <data version="2">
            <table name="diaro_locations">
            <r>
               <uid>1</uid>
               <title></title>
               <address>1 Two Road, New Old Street</address>
               <lat>50.000000</lat>
               <lng>-1.600000</lng>
               <zoom>5</zoom>
            </r>
            </table>
            </data>
            """)

        with NamedTemporaryFile(mode='w') as fp:
            fp.write(xml)
            fp.flush()
            diaro = Diaro(filename=fp.name)

        assert len(diaro.locations) == 1
        assert '1' in diaro.locations
        location = diaro.locations['1']
        assert location.title == ''
        assert location.address == '1 Two Road, New Old Street'
        assert location.lat == '50.000000'
        assert location.lng == '-1.600000'
        assert location.zoom == '5'

    def test_entry(self):
        xml = dedent("""\
            <data version="2">
            <table name="diaro_entries">
            <r>
               <uid>1</uid>
               <date>1434997052007</date>
               <tz_offset>+01:00</tz_offset>
               <title>title</title>
               <text>text</text>
               <folder_uid>2</folder_uid>
               <location_uid>3</location_uid>
               <tags></tags>
               <primary_photo_uid>4</primary_photo_uid>
            </r>
            </table>
            </data>
            """)

        with NamedTemporaryFile(mode='w') as fp:
            fp.write(xml)
            fp.flush()
            diaro = Diaro(filename=fp.name)

        assert len(diaro.entries) == 1
        assert '1' in diaro.entries
        entry = diaro.entries['1']
        assert entry.date == 1434997052007
        assert entry.tz_offset == '+01:00'
        assert entry.title == 'title'
        assert entry.text == 'text'
        assert entry.folder_uid == '2'
        assert entry.location_uid == '3'
        assert entry.tags == ''
        assert entry.primary_photo_uid == '4'

    def test_attachment(self):
        xml = dedent("""\
            <data version="2">
            <table name="diaro_attachments">
            <r>
               <uid>1</uid>
               <entry_uid>2</entry_uid>
               <type>photo</type>
               <filename>photo.jpg</filename>
               <position>1</position>
            </r>
            </table>
            </data>
            """)

        with NamedTemporaryFile(mode='w') as fp:
            fp.write(xml)
            fp.flush()
            diaro = Diaro(filename=fp.name)

        assert len(diaro.attachments) == 1
        assert '1' in diaro.attachments
        attachment = diaro.attachments['1']
        assert attachment.entry_uid == '2'
        assert attachment.type == 'photo'
        assert attachment.filename == 'photo.jpg'
        assert attachment.position == '1'

    def test_get_entries_for_folders(self):
        xml = dedent("""\
            <data version="2">
            <table name="diaro_folders">
            <r>
               <uid>2</uid>
               <title>Diary entries</title>
               <color>#000000</color>
               <pattern>pattern01</pattern>
            </r>
            <r>
               <uid>3</uid>
               <title>Quotes</title>
               <color>#111111</color>
               <pattern>pattern02</pattern>
            </r>
            </table>
            <table name="diaro_entries">
            <r>
               <uid>1</uid>
               <date>1434997052007</date>
               <tz_offset>+01:00</tz_offset>
               <title>title</title>
               <text>text</text>
               <folder_uid>2</folder_uid>
               <location_uid>3</location_uid>
               <tags></tags>
               <primary_photo_uid>4</primary_photo_uid>
            </r>
            <r>
               <uid>4</uid>
               <date>1434997052007</date>
               <tz_offset>+01:00</tz_offset>
               <title>not selected</title>
               <text>text</text>
               <folder_uid>7</folder_uid>
               <location_uid>3</location_uid>
               <tags></tags>
               <primary_photo_uid>4</primary_photo_uid>
            </r>
            <r>
               <uid>5</uid>
               <date>1434997052006</date>
               <tz_offset>+01:00</tz_offset>
               <title>Quote</title>
               <text>quote</text>
               <folder_uid>3</folder_uid>
               <location_uid>4</location_uid>
               <tags></tags>
               <primary_photo_uid></primary_photo_uid>
            </r>
            </table>
            </data>
            """)

        with NamedTemporaryFile(mode='w') as fp:
            fp.write(xml)
            fp.flush()
            diaro = Diaro(filename=fp.name)

        assert len(diaro.entries) == 3
        assert len(diaro.folders) == 2
        assert '2' in diaro.folders
        assert '3' in diaro.folders

        entries = diaro.get_entries_for_folders(None)
        assert len(entries) == 3
        assert entries[0].title == 'Quote'

        entries = diaro.get_entries_for_folders(['2'])
        assert len(entries) == 1
        assert entries[0].title == 'title'

        entries = diaro.get_entries_for_folders((x for x in ['2', '3']))
        assert len(entries) == 2
        assert entries[0].title == 'Quote'

    def get_attachments_for_entry(self, entry_uid):
        xml = dedent("""\
            <data version="2">
            <table name="diaro_attachments">
            <r>
               <uid>3</uid>
               <entry_uid>1</entry_uid>
               <type>photo</type>
               <filename>photo2.jpg</filename>
               <position>2</position>
            </r>
            <r>
               <uid>2</uid>
               <entry_uid>1</entry_uid>
               <type>photo</type>
               <filename>photo1.jpg</filename>
               <position>1</position>
            </r>
            </table>
            <table name="diaro_entries">
            <r>
               <uid>1</uid>
               <date>1434997052007</date>
               <tz_offset>+01:00</tz_offset>
               <title>title</title>
               <text>text</text>
               <folder_uid>2</folder_uid>
               <location_uid>3</location_uid>
               <tags></tags>
               <primary_photo_uid>4</primary_photo_uid>
            </r>
            </table>
            </data>
            """)

        with NamedTemporaryFile(mode='w') as fp:
            fp.write(xml)
            fp.flush()
            diaro = Diaro(filename=fp.name)

        attachments = diaro.get_attachments_for_entry('1')
        assert len(attachments) == 2
        assert attachment[0].position < attachment[1].position
