from odoo import models, fields


class Group(models.Model):

    _name = "group"
    _description = "Group"

    name = fields.Char(string="Name")
    month_listeners = fields.Integer(string="Month listeners")

    artist_id = fields.One2many(comodel_name="artist", inverse_name="group_id", string="Artist")
    song_id = fields.Many2many(comodel_name="song", string="Song")
    album_id = fields.One2many(comodel_name="album", inverse_name="group_id", string="Album")
