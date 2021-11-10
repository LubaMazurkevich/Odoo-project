from odoo import models, fields
from odoo.exceptions import UserError


class MusicUpdateTextWizard(models.TransientModel):

    _name = "music.update.text.wizard"
    _description = "Update Music Wizard"

    name = fields.Char(required=True, string="Name")
    month_listeners = fields.Integer(string="Month listeners")

    artist_ids = fields.One2many(comodel_name="api.artist", inverse_name="artist_group_id", string="Artist")
    song_ids = fields.Many2many(comodel_name="api.song", string="Song")
    album_ids = fields.One2many(comodel_name="api.album", inverse_name="album_group_id", string="Album")

    def update_polish_music_wizard(self):
        print(self.name)
        self.env["api.group"].browse(self._context.get("active_ids")).update({"name": self.name, "month_listeners": self.month_listeners,
                    "artist_ids": self.artist_ids, "song_ids": self.song_ids, "album_ids": self.album_ids})

