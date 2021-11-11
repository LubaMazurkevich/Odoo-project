from odoo import models, fields,api
from odoo.exceptions import UserError


class ApiArtist(models.Model):

    _name = "api.artist"
    _description = "Artist"

    name = fields.Char(required=True, string="Name")
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

    song_listeners = fields.Float(string="Song listeners", compute="_compute_total", store=True, digits=(32, 0))

    @api.model
    def create(self, vals):
        """
        Creating new artist if there is no artist with the same name
        """
        if self.env["api.artist"].search([("name", "=", vals["name"])]):
            raise UserError("This name for artist is already exist,please change it.")
        else:
            res = super(ApiArtist, self).create(vals)
            return res

    def write(self, vals):
        """
        Editing new artist if there is no artist with the same name
        """
        if "name" in vals and self.env["api.artist"].search([("name", "=", vals["name"])]) and vals["name"] != self.name:
            raise UserError("This name for artist is already exist,please change it.")
        else:
            res = super(ApiArtist, self).write(vals)
            return res

    def action_artist_redact(self):
        return {"type": "ir.actions.act_window",
                "res_model": "music.update.artist.wizard",
                "view_mode": "form",
                "target": "new",
                "context": {"default_name": self.name,
                            "default_song_ids": self.song_ids.ids}
                }

    @api.depends("song_ids.listeners")
    def _compute_total(self):
        for record in self:
            record.song_listeners += sum(record.song_ids.mapped("listeners"))