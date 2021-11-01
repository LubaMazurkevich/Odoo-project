from odoo import models, fields


class Group(models.Model):

    _name = "api.group"
    _description = "Group"

    name = fields.Char(string="Name")
    month_listeners = fields.Integer(string="Month listeners")

    artist_id = fields.One2many(comodel_name="artist", inverse_name="artist_group_id", string="Artist") #change here
    song_id = fields.Many2many(comodel_name="song", string="Song")
    album_id = fields.One2many(comodel_name="album", inverse_name="album_group_id", string="Album")
