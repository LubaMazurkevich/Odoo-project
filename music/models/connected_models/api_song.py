from odoo import models, fields ,api
from odoo.exceptions import UserError


class ApiSong(models.Model):

    _name = "api.song"
    _description = "Song"

    name = fields.Char(string="Name")
    listeners = fields.Integer(string="Listeners")
    duration = fields.Float(string="Duration")

    artist_ids = fields.Many2many(comodel_name="api.artist", string="Artist")
    song_group_ids = fields.Many2many(comodel_name="api.group", string="Group")
    album_id = fields.Many2one(comodel_name="api.album", string="Album")

    @api.model
    def create(self, vals):
        if self.env["api.song"].search([("name", "=", vals["name"])]):
            raise UserError("This name for song is already exist,please change it.")
        else:
            res = super(ApiSong, self).create(vals)
            return res

    def write(self, vals):
        if "name" in vals and self.env["api.song"].search([("name", "=", vals["name"])]):
            raise UserError("This name for song is already exist,please change it.")
        else:
            res = super(ApiSong, self).write(vals)
            return res

