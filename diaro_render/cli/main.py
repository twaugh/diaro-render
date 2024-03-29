"""
Render Diaro data format into HTML

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

from __future__ import absolute_import
from argparse import ArgumentParser
from diaro_render.data import Diaro
from datetime import datetime, timedelta
import os.path


class CLI(object):
    def __init__(self, args=None):
        parser = ArgumentParser('diaro-render')
        parser.add_argument('file', metavar='FILE', nargs=1,
                            help='path to DiaroBackup.xml')
        parser.add_argument('--folder', metavar='UID', action='append',
                            help='folder UID to filter by '
                            '(may be given more than once)')
        parser.add_argument('--mediapath', help='path to media files',
                            default='')
        parser.add_argument('--thumbsuffix', help='suffix for media thumbnails',
                            default='')
        parser.add_argument('--summary', action='store_true',
                            help='show summary instead of HTML output')
        parser.add_argument('--only-year', help='only render entries from year')
        self.namespace = parser.parse_args(args=args)

    def run(self):
        diaro = Diaro(self.namespace.file[0])
        entries = diaro.get_entries_for_folders(self.namespace.folder)

        if self.namespace.only_year:
            only_year = int(self.namespace.only_year)
            year_entries = [(datetime.fromtimestamp(entry.date / 1000.0).year,
                             entry) for entry in entries]
            entries = [entry for year, entry in year_entries
                       if year == only_year]

        if self.namespace.folder is None:
            # Display folders
            year_folder_uids = set(entry.folder_uid for entry in entries)
            year_folders = filter(lambda item: item[0] in year_folder_uids, diaro.folders.items())
            for uid, folder in year_folders:
                print("{uid}: {title}".format(uid=uid, title=folder.title))

            return

        if self.namespace.summary:
            for entry in entries:
                date = datetime.fromtimestamp(entry.date / 1000.0).isoformat(timespec='minutes')
                print("{date} [{folder}]: {title}".format(date=date,
                                                          folder=entry.folder_uid,
                                                          title=entry.title))
            return

        # render HTML
        mediapath = self.namespace.mediapath
        thumbsuffix = self.namespace.thumbsuffix
        for entry in entries:
            dt = datetime.fromtimestamp(entry.date / 1000.0)
            date = dt.strftime('%A %d %B %Y')
            time = dt.strftime('%H:%M')
            photo = ''
            attachments = diaro.get_attachments_for_entry(entry.uid)
            for attachment in attachments:
                assert attachment.type == 'photo'
                fmt = '<div><a href="{imgfullpath}"><img src="{imgthumbpath}" alt="" /></a></div>'
                filename, ext = os.path.splitext(attachment.filename)
                photo += fmt.format(
                    imgfullpath=os.path.join(mediapath,
                                             attachment.filename),
                    imgthumbpath=os.path.join(mediapath,
                                              filename + thumbsuffix + ext))

            print("""\
<div>
  <!-- entry -->
  <h3>{title}</h3>
  <small><b>{date}</b> <i>{time}</i> ({foldertitle})</small>
  <p>{text}</p>
  {photo}
</div>
""".format(date=date, time=time,
           foldertitle=diaro.folders[entry.folder_uid].title,
           title=entry.title,
           text=entry.text,
           photo=photo))

def main():
    CLI().run()


if __name__ == '__main__':
    # Run directly:
    # python -m diaro_render.cli.main <FILE>
    main()
