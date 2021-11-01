
from odoo import models, fields


class Song(models.Model):

    _name = "song"
    _description = "Song"

    name = fields.Char(string="Name")
    listeners = fields.Integer(string="Listeners")
    duration = fields.Char(string="Duration")

    artist_id = fields.Many2many(comodel_name="artist", string="Artist")
    song_group_id = fields.Many2many(comodel_name="api.group", string="Group") #change here
    album_id = fields.Many2one(comodel_name="album", string="Album")
