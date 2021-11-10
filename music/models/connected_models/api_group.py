from odoo import models, fields,api
from odoo.exceptions import UserError


class ApiGroup(models.Model):

    _name = "api.group"
    _description = "Group"

    name = fields.Char(required=True, string="Name")
    month_listeners = fields.Integer(string="Month listeners")

    artist_ids = fields.One2many(comodel_name="api.artist", inverse_name="artist_group_id", string="Artist")
    song_ids = fields.Many2many(comodel_name="api.song", string="Song")
    album_ids = fields.One2many(comodel_name="api.album", inverse_name="album_group_id", string="Album")

    @api.model
    def create(self, vals):
        """
        Creating new group if there is no group with the same name
        """
        if self.env["api.group"].search([("name", "=", vals["name"])]):
            raise UserError("This name for group is already exist,please change it.")
        else:
            res = super(ApiGroup, self).create(vals)
            return res

    def write(self, vals):
        """
        Editing new group if there is no group with the same name
        """
        if "name" in vals and self.env["api.group"].search([("name", "=", vals["name"])]) and vals["name"] != self.name:
            raise UserError("This name  for group is already exist,please change it.")
        else:
            res = super(ApiGroup, self).write(vals)
            return res


