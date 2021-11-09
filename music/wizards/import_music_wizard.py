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
        """
        Loading file and parsing Artists and Groups.
        """
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
        """
        Parsing artists.
        """
        for artist in artists_root.iterfind(".//artist"):
            self.parse_artist(artist, group)

    def parse_groups(self, groups_root):
        """
        Parsing groups.
        """
        for group in groups_root.iterfind(".//group"):
            self.parse_group(group)

    def update_artist(self, artist_id, artist_dct, artist_root, group=None):
        """
        Update artist.
        """
        artist_id.update(artist_dct)
        if group:
            artist_id.artist_group_id = group.id
        else:
            try:
                group_id = self.env.ref('music.group_solo_artist').id
                artist_id.artist_group_id = group_id
            except:
                _logger.warning(f"Parsing error for music file:solo artist group not found")
        artist_singles = artist_root.find("singles")
        if artist_singles:
            self.parse_singles(artist_singles, artist=artist_id)
        artist_albums = artist_root.find("albums")
        if artist_albums:
            self.parse_albums(artist_albums, artist=artist_id)

    def get_artist(self, artist_name):
        """
        Get artist.
        """
        artist_id = self.env["api.artist"].search([("name", "=", artist_name)])
        if not artist_id:
            artist_id = self.env["api.artist"].create({"name": artist_name})
        return artist_id

    def parse_artist(self, artist_root, group=None):
        """
        Parsing artist.
        """
        artist_dct = {}
        artist_name = artist_root.find("name")
        if artist_name is not None and artist_name.text is not None:
            artist_dct["name"] = artist_name.text.strip()
        else:
            _logger.warning(f"Parsing error for music file: name for artist")
        artist_month_listeners = artist_root.find("month_listeners")
        if artist_month_listeners is not None and artist_month_listeners.text is not None:
            artist_dct["month_listeners"] = artist_month_listeners .text.strip()
        else:
            _logger.warning(f"Parsing error for music file:month listeners for artist")
        artist_age = artist_root.find("age")
        if artist_age is not None and artist_age.text is not None:
            artist_dct["age"] = artist_age.text.strip()
        else:
            _logger.warning(f"Parsing error for music file:age for artist")
        artist_sex = artist_root.find("sex")
        if artist_sex is not None and artist_sex.text is not None:
            artist_dct["sex"] = artist_sex.text.strip()
        else:
            _logger.warning(f"Parsing error for music file:sex for artist")
        artist_country = artist_root.find("country")
        if artist_country is not None and artist_country.text is not None:
            res_country_id = self.env["res.country"].search(['|', ("name", "=", artist_country.text.strip()), ("code", "=", artist_country.text.strip())])
            if res_country_id:
                artist_dct["country_id"] = res_country_id.id
            else:
                _logger.warning(f"Parsing error for music file:country for artist")
        if "name" in artist_dct:
            artist_id = self.get_artist(artist_dct["name"])
            self.update_artist(artist_id, artist_dct, artist_root, group)

    def parse_singles(self, single_root, group=None, artist=None):
        """
        Parsing singles.
        """
        for single in single_root.iterfind(".//songs"):
            self.parse_songs(single, group, artist)

    def parse_songs(self, songs_root, group=None, artist=None, album=None):
        """
        Parsing songs.
        """
        for songs in songs_root.iterfind(".//song"):
            self.parse_song(songs, group, artist, album)

    def parse_albums(self, albums_root, group=None, artist=None, songs=None):
        """
        Parsing albums.
        """
        for album in albums_root.iterfind(".//album"):
            self.parse_album(album, group, artist, songs)

    def update_group(self, group_id, group_dct, group_root):
        """
        Updating group and its data.
        """
        group_id.update(group_dct)
        group_artists = group_root.find("artists")
        if group_artists:
            self.parse_artists(group_artists, group=group_id)
        group_albums = group_root.find("albums")
        if group_albums:
            self.parse_albums(group_albums, group=group_id)
        group_singles = group_root.find("singles")
        if group_singles:
            self.parse_singles(group_singles, group=group_id)

    def get_group(self, group_name):
        """
        Get group.
        """
        group_id = self.env["api.group"].search([("name", "=", group_name)])
        if not group_id:
            group_id = self.env["api.group"].create({"name": group_name})
        return group_id
#bb
    def parse_group(self, group_root):
        """
        Parsing group.
        """
        group_dct = {}
        group_month_listeners = group_root.find("month_listeners")
        if group_month_listeners is not None and group_month_listeners.text is not None:
            group_dct["month_listeners"] = group_month_listeners.text.strip()
        else:
            _logger.warning(f"Parsing error for music file :group month listeners")
        group_name = group_root.find("name")
        if group_name is not None and group_name.text is not None:
            group_dct["name"] = group_name.text.strip()
        else:
            _logger.warning(f"Parsing error for music file:group name")
        if "name" in group_dct:
            group_id = self.get_group(group_dct["name"])
            self.update_group(group_id, group_dct, group_root)

    def parse_member(self, member_root, song):
        """
        Parsing member.
        """
        member_name = member_root.find("name")
        if member_name is not None and member_name.text is not None:
            artist_id = self.env["api.artist"].search([("name", "=", member_name.text.strip())]).id
            if artist_id:
                song.artist_ids = [(4, artist_id, 0)]
            group_id = self.env["api.group"].search([("name", "=", member_name.text.strip())]).id
            if group_id:
                song.song_group_ids = [(4, group_id, 0)]

    def parse_members(self, members_root, song):
        """
        Parsing members.
        """
        for members in members_root.iterfind(".//member"):
            self.parse_member(members, song)

    def get_song(self, song_name):
        """
        Get song.
        """
        song_id = self.env["api.song"].search([("name", "=", song_name)])
        if not song_id:
            song_id = self.env["api.song"].create({"name": song_name})
        return song_id

    def update_song(self, song_id, song_dct, song_root, group, artist, album):
        """
        Update song.
        """
        song_id.update(song_dct)
        if group:
            song_id.song_group_ids = [(4, group.id, 0)]
        if artist:
            song_id.artist_ids = [(4, artist.id, 0)]
        if album:
            song_id.album_id = album.id
        song_members = song_root.find("members")
        if song_members:
            self.parse_members(song_members, song=song_id)

    def parse_song(self, song_root, group, artist, album):
        """
        Parsing song.
        """
        song_dct = {}
        song_name = song_root.find("name")
        if song_name is not None and song_name.text is not None:
            song_dct["name"] = song_name.text.strip()
        else:
            _logger.warning(f"Parsing error for music file:song name")
        song_duration = song_root.find("duration")
        if song_duration is not None and song_duration.text is not None:
            song_dct["duration"] = float(song_duration.text.strip().replace(":", "."))
        else:
            _logger.warning(f"Parsing error for music file:song duration")
        song_listeners = song_root.find("listeners")
        if song_listeners is not None and song_listeners.text is not None:
            song_dct["listeners"] = song_listeners.text.strip()
        else:
            _logger.warning(f"Parsing error for music file:song listeners")
        if "name" in song_dct:
            song_id = self.get_song(song_dct["name"])
            self.update_song(song_id, song_dct, song_root, group, artist, album)

    def update_album(self, album_id, album_dct, album_root, group, artist, songs):
        """
        Update album.
        """
        album_id.update(album_dct)
        album_songs = album_root.find("songs")
        if album_songs:
            self.parse_songs(album_songs, album=album_id)
        if group:
            album_id.album_group_id = group.id
        if artist:
            album_id.artist_id = artist.id
        if songs:
            album_id.song_ids = [(4, songs.id, 0)]

    def get_album(self, album_name):
        """
        Get album.
        """
        album_id = self.env["api.album"].search([("name", "=", album_name)])
        if not album_id:
            album_id = self.env["api.album"].create({"name": album_name})
        return album_id

    def parse_album(self, album_root, group, artist, songs):
        """
        Parsing album.
        """
        album_dct = {}
        album_name = album_root.find("name")
        if album_name is not None and album_name.text is not None:
            album_dct["name"] = album_name.text.strip()
        album_release_date = album_root.find("release_date")
        if album_release_date is not None and album_release_date.text is not None:
            date_str = album_release_date.text.strip()
            album_dct["release_date"] = datetime.strptime(date_str, '%m-%d-%Y')
        else:
            _logger.warning(f"Parsing error for music file:album release date")
        if "name" in album_dct:
            album_id = self.get_album(album_dct["name"])
            self.update_album(album_id, album_dct, album_root, group, artist, songs)
