from odoo import models, fields,api
from odoo.exceptions import UserError


class ApiArtist(models.Model):

    _name = "api.artist"
    _description = "Artist"

    name = fields.Char(string="Name")
    age = fields.Integer(string="Age")
    sex = fields.Selection([
        ('male', "Male"),
        ("female", "Female"),
        ("other", "other"),
    ])
    country_id = fields.Many2one("res.country", string="Country")
    month_listeners = fields.Integer(string="Month listeners")

    album_ids = fields.One2many(comodel_name="api.album", inverse_name="artist_id", string="Album")
    song_ids = fields.Many2many(comodel_name="api.song", string="Song")
    artist_group_id = fields.Many2one(comodel_name="api.group", string="Group")

    @api.model
    def create(self, vals):
        if self.env["api.artist"].search([("name", "=", vals["name"])]):
            raise UserError("This name is already exist,please change it.")
        else:
            res = super(ApiArtist, self).create(vals)
            return res

    def write(self, vals):
        if self.env["api.artist"].search([("name", "=", vals["name"])]):
            raise UserError("This name is already exist,please change it.")
        else:
            res = super(ApiArtist, self).write(vals)
            return res



