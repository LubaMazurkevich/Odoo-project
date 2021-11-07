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
        """
        Creating new song if there is no artist with the same name and name is correct
        """
        if self.env["api.song"].search([("name", "=", vals["name"])]):
            raise UserError("This name for song is already exist,please change it.")
        elif vals["name"] is False:
            raise UserError("Song name can't be empty")
        else:
            res = super(ApiSong, self).create(vals)
            return res

    def write(self, vals):
        """
        Editing new song if there is no artist with the same name and name is correct
        """
        if "name" in vals and self.env["api.song"].search([("name", "=", vals["name"])]):
            raise UserError("This name for song is already exist,please change it.")
        elif "name" in vals and vals["name"] is False:
            raise UserError("Song name can't be empty")
        else:
            res = super(ApiSong, self).write(vals)
            return res

