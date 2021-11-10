from odoo import models, fields
from odoo.exceptions import UserError


class MusicUpdateArtistWizard(models.TransientModel):

    _name = "music.update.artist.wizard"
    _description = "Update Music Wizard"

    name = fields.Char(required=True, string="Name")
    song_ids = fields.Many2many(comodel_name="api.song", string="Song")
    song_listeners = fields.Integer(string="Song listeners")

    def update_artist_wizard(self):
        self.env["api.group"].browse(self._context.get("active_ids")).update({"name": self.name, "song_ids": self.song_ids,"song_listeners ": self.song_listeners })
