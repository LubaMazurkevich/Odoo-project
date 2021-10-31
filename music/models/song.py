
from odoo import models, fields


class Song(models.Model):

    _name = "song"
    _description = "Song"

    name = fields.Char(string="Name")
    listeners = fields.Integer(string="Listeners")
    duration = fields.Char(string="Duration")

    artist_ids = fields.Many2many(comodel_name="artist", string="Artist")
    group_ids = fields.Many2many(comodel_name="group", string="Group")
    album_id = fields.Many2one(comodel_name="album", string="Album")
