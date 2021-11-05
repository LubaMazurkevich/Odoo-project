from odoo import models, fields


class ApiSong(models.Model):

    _name = "api.song"
    _description = "Song"

    name = fields.Char(string="Name")
    listeners = fields.Integer(string="Listeners")
    duration = fields.Float(string="Duration")

    artist_ids = fields.Many2many(comodel_name="api.artist", string="Artist")
    song_group_ids = fields.Many2many(comodel_name="api.group", string="Group")
    album_id = fields.Many2one(comodel_name="api.album", string="Album")
