from odoo import models, fields,api
from odoo.exceptions import UserError


class ApiGroup(models.Model):

    _name = "api.group"
    _description = "Group"

    name = fields.Char(string="Name")
    month_listeners = fields.Integer(string="Month listeners")

    artist_ids = fields.One2many(comodel_name="api.artist", inverse_name="artist_group_id", string="Artist")
    song_ids = fields.Many2many(comodel_name="api.song", string="Song")
    album_ids = fields.One2many(comodel_name="api.album", inverse_name="album_group_id", string="Album")

    @api.model
    def create(self, vals):
        '''
         Create new group with сhecking the name of group with the same/empty name
         '''
        if self.env["api.group"].search([("name", "=", vals["name"])]):
            raise UserError("This name for group is already exist,please change it.")
        if vals["name"] is False:
            raise UserError("Name for group can't be empty")
        else:
            res = super(ApiGroup, self).create(vals)
            return res

    def write(self, vals):
        '''
        Edit group with сhecking the name of group with the same/empty name
        '''
        if "name" in vals and self.env["api.group"].search([("name", "=", vals["name"])]):
            raise UserError("This name  for group is already exist,please change it.")
        if "name" in vals and vals["name"] is False:
            raise UserError("Name for group can't be empty")
        else:
            res = super(ApiGroup, self).write(vals)
            return res