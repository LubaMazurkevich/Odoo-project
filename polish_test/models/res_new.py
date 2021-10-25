from odoo import models, fields , api
from datetime import datetime


class ResPartner(models.Model):

    _inherit = "res.partner"

    res_new_description = fields.Char(string='Res partner description', required=True)