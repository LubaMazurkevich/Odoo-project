from odoo import models, fields
import base64
from datetime import datetime
import xml.etree.ElementTree as ET
import logging
_logger = logging.getLogger(__name__)


class ImportMusicWizard(models.TransientModel):

    _name = "import.music.wizard"
    _description = "Create Music Wizard"

    file = fields.Binary(string="File", required=True)

    def upload_file_wizard(self):
        file = base64.b64decode(self.file)
        file_string = file.decode('utf-8')
        root = ET.fromstring(file_string)

        artists_root = root.find("Artists")
        if artists_root:
            self.parse_artists(artists_root)
        groups_root = root.find("Groups")
        if groups_root:
            self.parse_groups(groups_root)

    def parse_artists(self, artists_root, group=None):
        for artist in artists_root.iterfind(".//artist"):
            self.make_artist(artist, group)

    def parse_groups(self, groups_root):
        for group in groups_root.iterfind(".//group"):
            self.make_group(group)

    def make_artist(self, artist_root, group):
        artist_dct = {}
        artist_name = artist_root.find("name")
        if artist_name is not None:
            artist_dct["name"] = artist_name.text.strip()
        else:
            _logger.warning(f"Parsing error for music file: name for artist")

        artist_month_listeners = artist_root.find("month_listeners")
        if artist_month_listeners is not None:
            artist_dct["month_listeners"] = artist_month_listeners .text.strip()
        else:
            _logger.warning(f"Parsing error for music file:month listeners for artist")
        artist_age = artist_root.find("age")
        if artist_age is not None:
            artist_dct["age"] = artist_age.text.strip()
        else:
            _logger.warning(f"Parsing error for music file:age for artist")
        artist_sex = artist_root.find("sex")
        if artist_sex is not None:
            artist_dct["sex"] = artist_sex.text.strip()
        else:
            _logger.warning(f"Parsing error for music file:sex for artist")

        artist_country = artist_root.find("country")
        if artist_country is not None:
            res_country_id = self.env["res.country"].search(['|', ("name", "=", artist_country.text.strip()), ("code", "=", artist_country.text.strip())])
            if res_country_id:
                artist_dct["country_id"] = res_country_id.id
            else:
                _logger.warning(f"Parsing error for music file:country for artist")

        artist_singles = artist_root.find("singles")
        artist_albums = artist_root.find("albums")

        if artist_dct or artist_singles or artist_albums or group:
            artist = self.env["api.artist"].create(artist_dct)
            if group:
                artist.artist_group_id = group.id
            if artist_singles:
                self.make_singles(artist_singles, artist=artist)
            if artist_albums:
                self.make_albums(artist_albums, artist=artist)

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
        group_dct = {}
        group_month_listeners = group_root.find("month_listeners")
        if group_month_listeners is not None:
            group_dct["month_listeners"] = group_month_listeners.text.strip()
        else:
            _logger.warning(f"Parsing error for music file :group month listeners")
        group_name = group_root.find("name")
        if group_name is not None:
            group_dct["name"] = group_name.text.strip()
        else:
            _logger.warning(f"Parsing error for music file:group name")

        group_artists = group_root.find("artists")
        group_albums = group_root.find("albums")
        group_singles = group_root.find("singles")

        if group_dct or group_artists or group_albums or group_singles:
            group = self.env["api.group"].create(group_dct)
            if group_artists:
                self.parse_artists(group_artists, group=group)
            if group_albums:
                self.make_albums(group_albums, group=group)
            if group_singles:
                self.make_singles(group_singles, group=group)

    def make_member(self, member_root, song=None):
        member_name = member_root.find("name")
        if member_name is not None:
            artist_id = self.env["api.artist"].search([("name", "=", member_name.text.strip())]).id
            print(artist_id)
            if artist_id:
                print("here")
                song.artist_ids = [(4, artist_id, 0)]
            else:
                print("and here")
                pass
            group_id = self.env["api.group"].search([("name", "=", member_name.text.strip())])
            if group_id:
                song.song_group_ids = [(4, group_id, 0)]
            else:
                pass

    def make_members(self, members_root, song=None):
        for members in members_root.iterfind(".//member"):
            self.make_member(members, song)

    def make_song(self, song_root, group=None, artist=None, album=None): #проверка на дубликат есть!
        song_dct = {}
        song_name = song_root.find("name")
        if song_name is not None:
            song_dct["name"] = song_name.text.strip()
        else:
            _logger.warning(f"Parsing error for music file:song name")
        song_duration = song_root.find("duration")
        if song_duration is not None:
            song_dct["duration"] = float(song_duration.text.strip().replace(":", "."))
        else:
            _logger.warning(f"Parsing error for music file:song duration")
        song_listeners = song_root.find("listeners")
        if song_listeners is not None:
            song_dct["listeners"] = song_listeners.text.strip()
        else:
            _logger.warning(f"Parsing error for music file:song listeners")
        song_members = song_root.find("members")
        if song_dct or song_members:
            song = self.env["api.song"].search([("name", "=", song_dct["name"])])
            if song:
                song.update(song_dct)
            else:
                song = self.env["api.song"].create(song_dct)
            if group:
                song.song_group_ids = [(4, group.id, 0)]
            if artist:
                song.artist_ids = [(4, artist.id, 0)]
            if album:
                song.album_id = album.id
            if song_members:
                self.make_members(song_members, song=song)

    def make_album(self, album_root, group, artist, songs): #проверка на дубликат
        album_dct = {}
        album_name = album_root.find("name")
        if album_name is not None:
            album_dct["name"] = album_name.text.strip()
        album_release_date = album_root.find("release_date")
        if album_release_date is not None:
            date_str = album_release_date.text.strip()
            album_dct["release_date"] = datetime.strptime(date_str, '%m-%d-%Y')
        else:
            _logger.warning(f"Parsing error for music file:album release date")
        album_songs = album_root.find("songs")
        if album_dct or album_songs:
            album = self.env["api.album"].search([("name", "=", album_dct["name"])])
            if album:
                album.update(album_dct)
            else:
                album = self.env["api.album"].create(album_dct)
            if album_songs:
                self.make_songs(album_songs, album=album)
            if group:
                album.album_group_id = group.id
            if artist:
                album.artist_id = artist.id
            if songs:
                album.song_ids = [(4, songs.id, 0)]