from odoo import models, fields , api


class ResPartner(models.Model):

    _inherit = "res.partner"

    description = fields.Char(string="Description", required=True)
