import base64

from odoo import models, fields
import xml.etree.ElementTree as ET


class ImportMusicWizard(models.TransientModel):

    _name = "import.music.wizard"
    _description = "Create Music Wizard"

    file = fields.Binary(string="File", required=True)

    def upload_file_wizard(self):
        file = base64.b64decode(self.file)
        file_string = file.decode('utf-8')
        root = ET.fromstring(file_string)

        def parse_artists(artists_root, group=None):
            for i in artists_root:
                if i.tag == 'artist':
                    make_artist(i, group)

        def make_artist(artist_root, group):
            artist = self.env["artist"].create({})
            for i in artist_root:
                if i.tag == 'name':
                    artist.name = i.text.strip()
                if i.tag == 'month_listeners':
                    artist.month_listeners = i.text.strip()
                if i.tag == 'age':
                    artist.age = i.text.strip()
                if i.tag == "sex":
                    artist.sex = i.text.strip()
                if i.tag == "country":
                    artist.country_id = i.text.strip()
                if i.tag == "singles":
                    make_singles(i, artist=artist)
                if i.tag == "albums":
                    make_albums(i, artist=artist)
            if group is not None:
                artist.artist_group_id = group.id   #change here

        def make_singles(single_root, group=None, artist=None):
            for i in single_root:
                if i.tag == "songs":
                    make_songs(i, group, artist)

        def make_songs(songs_root, group=None, artist=None, album=None):
            for i in songs_root:
                if i.tag == "song":
                    make_song(i, group, artist, album)

        def make_song(song_root, group=None, artist=None, album=None):
            song = self.env["song"].create({})
            for i in song_root:
                if i.tag == "name":
                    song.name = i.text.strip()
                if i.tag == "duration":
                    song.duration = i.text.strip()
                if i.tag == "listeners":
                    song.listeners = i.text.strip()
            if group != None:
                song.song_group_id = [(4, group.id, 0)]  #change here
            if artist != None:
                song.artist_id = [(4, artist.id, 0)]
            if album != None:
                song.album_id = album.id

        def make_albums(albums_root, group=None, artist=None, songs=None):
            for i in albums_root:
                if i.tag == "album":
                    make_album(i, group, artist, songs)

        def make_album(album_root, group, artist, songs):
            album = self.env["album"].create({})
            for i in album_root:
                if i.tag == "name":
                    album.name = i.text.strip()
                if i.tag == "songs":
                    make_songs(i, album=album)
                if i.tag == "release_date":
                    new_release_date=i.text.strip()
                    album.release_date = new_release_date[6:] + "-" + new_release_date[0:5]
            if group is not None:
                album.album_group_id = group.id  #change here
            if artist is not None:
                album.artist_id = artist.id
            if songs is not None:
                album.song_id = songs.id

        def make_group(group_root):
            group = self.env["api.group"].create({})
            for i in group_root:
                if i.tag == "month_listeners":
                    group.month_listeners = i.text.strip()
                if i.tag == "name":
                    group.name = i.text.strip()
                if i.tag == "artists":
                    parse_artists(i, group=group)
                if i.tag == "albums":
                    make_albums(i, group=group)
                if i.tag == "singles":
                    make_singles(i, group=group)

        def parse_groups(groups_root):
            for i in groups_root:
                if i.tag == "group":
                    make_group(i)

        for i in root:
            if i.tag == "Artists":
                parse_artists(i)
            if i.tag == "Groups":
                parse_groups(i)







