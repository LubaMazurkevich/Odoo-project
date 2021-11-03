import base64

from odoo import models, fields
import xml.etree.ElementTree as ET
import logging
_logger = logging.getLogger(__name__)
from datetime import datetime
import lxml.etree


class ImportMusicWizard(models.TransientModel):

    _name = "import.music.wizard"
    _description = "Create Music Wizard"

    file = fields.Binary(string="File", required=True)

    def upload_file_wizard(self):
        file = base64.b64decode(self.file)
        file_string = file.decode('utf-8')
        root = ET.fromstring(file_string)
        try:
            artists_root = root.find("Artists")
            self.parse_artists(artists_root)
        except:
            pass
        try:
            groups_root = root.find("Groups")
            self.parse_groups(groups_root)
        except:
            pass

    def parse_artists(self, artists_root, group=None):
        for artist in artists_root.iterfind(".//artist"):
            self.make_artist(artist, group)

    def parse_groups(self, groups_root):
        for group in groups_root.iterfind(".//group"):
            self.make_group(group)

    def make_artist(self, artist_root, group):
        artist = self.env["artist"].create({})
        try:
            atrist_name = artist_root.find("name")
            artist.name = atrist_name.text.strip()
        except:
            _logger.warning(f"Parsing error for music file:name for artist {artist.name}")
        try:
            artist_month_listeners = artist_root.find("month_listeners")
            artist.month_listeners = artist_month_listeners .text.strip()
        except:
            _logger.warning(f"Parsing error for music file:month listeners for artist {artist.name}")
        try:
            artist_age = artist_root.find("age")
            artist.age = artist_age.text.strip()
        except:
            _logger.warning(f"Parsing error for music file:age for artist {artist.name}")
        try:
            artist_sex = artist_root.find("sex")
            artist.sex = artist_sex.text.strip()
        except:
            _logger.warning(f"Parsing error for music file:sex for artist {artist.name}")
        try:
            artist_country = artist_root.find("country")
            id = self.env["res.country"].search(['|', ("name", "=", artist_country.text.strip()), ("code", "=", artist_country.text.strip())])
            if id:
                artist.country_id = id
            else:
                _logger.warning(f"Parsing error for music file.Country for artist {artist.name} was not found.")
        except:
            pass
        try:
            artist_singles = artist_root.find("singles")
            self.make_singles(artist_singles, artist=artist)
        except:
            pass
        try:
            artist_albums = artist_root.find("albums")
            self.make_albums(artist_albums, artist=artist)
        except:
            pass
        if group:
            artist.artist_group_id = group.id

    def make_singles(self, single_root, group=None, artist=None):
        for single in single_root.iterfind(".//songs"):
            self.make_songs(single, group, artist)

    def make_songs(self, songs_root, group=None, artist=None, album=None):
        for songs in songs_root.iterfind(".//song"):
            self.make_song(songs, group, artist, album)

    def make_albums(self, albums_root, group=None, artist=None, songs=None):
        for album in albums_root.iterfind(".//album"):
            self.make_album(album, group, artist, songs)

    def make_group(self, group_root):
        group = self.env["api.group"].create({})
        try:
            group_month_listeners = group_root.find("month_listeners")
            group.month_listeners = group_month_listeners.text.strip()
        except:
            _logger.warning(f"Parsing error for music file :group month listeners")
        try:
            group_name = group_root.find("name")
            group.name = group_name.text.strip()
        except:
            _logger.warning(f"Parsing error for music file:group name")
        try:
            group_artists = group_root.find("artists")
            self.parse_artists(group_artists, group=group)
        except:
            pass
        try:
            group_albums = group_root.find("albums")
            self.make_albums(group_albums, group=group)
        except:
            pass
        try:
            group_singles = group_root.find("singles")
            self.make_singles(group_singles, group=group)
        except:
            pass

    def make_song(self, song_root, group=None, artist=None, album=None):
        song = self.env["song"].create({})
        try:
            song_name = song_root.find("name")
            song.name = song_name.text.strip()
        except:
            _logger.warning(f"Parsing error for music file:song name")
        try:
            song_duration = song_root.find("duration")
            song.duration = song_duration.text.strip()
        except:
            _logger.warning(f"Parsing error for music file:song duration")
        try:
            song_listeners = song_root.find("listeners")
            song.listeners = song_listeners.text.strip()
        except:
            _logger.warning(f"Parsing error for music file:song listeners")
        if group:
            song.song_group_id = [(4, group.id, 0)]
        if artist:
            song.artist_id = [(4, artist.id, 0)]
        if album:
            song.album_id = album.id

    def make_album(self, album_root, group, artist, songs):
        album = self.env["album"].create({})
        try:
            album_songs = album_root.find("songs")
            self.make_songs(album_songs, album=album)
        except:
            pass
        try:
            album_name = album_root.find("name")
            album.name = album_name.text.strip()
        except:
            _logger.warning(f"Parsing error for music file:album name")
        try:
            album_release_date = album_root.find("release_date")
            date_str = album_release_date.text.strip()
            album.release_date = datetime.strptime(date_str, '%m-%d-%Y')
        except:
            _logger.warning(f"Parsing error for music file:album release date")
        if group:
            album.album_group_id = group.id
        if artist:
            album.artist_id = artist.id
        if songs:
            album.song_id = [(4, songs.id, 0)]







