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
