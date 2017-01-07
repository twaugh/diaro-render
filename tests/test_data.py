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
            d = Diaro(filename=fp.name)
