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
        parser.add_argument('--folder', metavar='UID',
                            help='folder UID to filter by')
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
        if self.namespace.folder is None:
            # Display folders
            for uid, folder in diaro.folders.items():
                print("{uid}: {title}".format(uid=uid, title=folder.title))

            return

        entries = diaro.get_entries_for_folder(self.namespace.folder)

        if self.namespace.only_year:
            only_year = int(self.namespace.only_year)
            year_entries = [(datetime.fromtimestamp(entry.date / 1000.0).year,
                             entry) for entry in entries]
            entries = [entry for year, entry in year_entries
                       if year == only_year]

        if self.namespace.summary:
            for entry in entries:
                print("{date}: {title}".format(date=entry.date,
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
                fmt = '<div><a href="{imgfullpath}"><img src="{imgthumbpath}" alt="" /><a></div>'
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
  <b>{date}</b> <i>{time}</i>
  <p>{text}</p>
  {photo}
</div>
""".format(date=date, time=time,
           title=entry.title,
           text=entry.text,
           photo=photo))

def main():
    CLI().run()


if __name__ == '__main__':
    # Run directly:
    # python -m diaro_render.cli.main <FILE>
    main()
