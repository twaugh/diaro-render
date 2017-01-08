"""
Render Diaro data format into HTML - tests

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

from diaro_render.cli.main import CLI
from textwrap import dedent
from tempfile import NamedTemporaryFile


class TestDiaroCLI(object):
    def test_minimal(self):
        xml = dedent("""\
            <data version="2">
            </data>
            """)

        with NamedTemporaryFile(mode='w') as fp:
            fp.write(xml)
            fp.flush()
            cli = CLI([fp.name])
            cli.run()
