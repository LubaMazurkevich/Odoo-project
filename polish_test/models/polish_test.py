from odoo import models, fields


class PolishTest(models.Model):
    _name = "polish.test"

    name = fields.Char(string='name')

