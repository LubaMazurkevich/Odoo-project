from odoo import models, fields


class MusicUpdateArtistWizard(models.TransientModel):

    _name = "music.update.artist.wizard"
    _description = "Update Music Wizard"

    name = fields.Char(required=True, string="Name")
    song_ids = fields.Many2many(comodel_name="api.song", string="Song")
    song_listeners = fields.Float(string="Song listeners")

    def update_artist_wizard(self):
        song_listeners = sum(self.song_ids.mapped("listeners"))
        self.env["api.artist"].browse(self._context.get("active_ids")).update({"name": self.name, "song_ids": self.song_ids, "song_listeners": song_listeners})






















        # song_listeners = 0
        # for song in self.song_ids:
        #     song_listeners += song.listeners