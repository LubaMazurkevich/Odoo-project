from odoo import models, fields


class Album(models.Model):

    _name = "album"
    _description = "Album"

    name = fields.Char(string="Name")
    release_date = fields.Date(string="Date of release")

    artist_id = fields.Many2one(comodel_name="artist", string="Artist")
    album_group_id = fields.Many2one(comodel_name="api.group", string="Group") #change here
    song_id = fields.One2many(comodel_name="song", inverse_name="album_id", string="Song")