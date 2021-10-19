from odoo import models, fields
from datetime import datetime


class PolishTest(models.Model):
    _name = "polish.test"
    _description ="Polish Test"

    name = fields.Char(string='Name', required=True)
    age = fields.Integer(string='Age')
    gender = fields.Selection([
        ('male', "Male"),
        ("female", "Female"),
        ("other", "other"),
    ], required=True, default='male')
    note = fields.Text(string="Description")


