
from odoo import models, fields


class Artist(models.Model):

    _name = "artist"
    _description = "Artist"

    name = fields.Char(string="Name")
    age = fields.Integer(string="Age")
    sex = fields.Selection([
        ('male', "Male"),
        ("female", "Female"),
        ("other", "other"),
    ], required=True)
    country_id = fields.Many2one("res.country", string="Country")
    month_listeners = fields.Integer(string="Month listeners")

    album_id = fields.One2many(comodel_name="album", inverse_name="artist_id", string="Album")
    song_id = fields.Many2many(comodel_name="song", string="Song")
    group_id = fields.Many2one(comodel_name="group", string="Group")





