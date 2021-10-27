from odoo import models, fields


class ResPartner(models.Model):

    _inherit = "res.partner"

    description = fields.Char(string="Description")
    is_polish = fields.Boolean()



