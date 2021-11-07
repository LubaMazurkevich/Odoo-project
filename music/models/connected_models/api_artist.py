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
    month_listeners = fields.Integer(string="Month listeners")

    country_id = fields.Many2one("res.country", string="Country")
    album_ids = fields.One2many(comodel_name="api.album", inverse_name="artist_id", string="Album")
    song_ids = fields.Many2many(comodel_name="api.song", string="Song")
    artist_group_id = fields.Many2one(comodel_name="api.group", string="Group")

    @api.model
    def create(self, vals):
        """
        Creating new artist if there is no artist with the same name and name is correct
        """
        if self.env["api.artist"].search([("name", "=", vals["name"])]):
            raise UserError("This name for artist is already exist,please change it.")
        elif vals["name"] is False:
            raise UserError("Artist name can't be empty")
        else:
            res = super(ApiArtist, self).create(vals)
            return res

    def write(self, vals):
        """
        Editing new artist if there is no artist with the same name and name is correct
        """
        if "name" in vals and self.env["api.artist"].search([("name", "=", vals["name"])]):
            raise UserError("This name for artist is already exist,please change it.")
        elif "name" in vals and vals["name"] is False:
            raise UserError("Artist name can't be empty")
        else:
            res = super(ApiArtist, self).write(vals)
            return res



