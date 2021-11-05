from odoo import models, fields


class ResPartner(models.Model):

    _inherit = "res.partner"

    description = fields.Char(string="Description")
    is_polish = fields.Boolean()
    polish_id = fields.Many2one(comodel_name="polish.test", string="Polish")



