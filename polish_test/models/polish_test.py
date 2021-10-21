from odoo import models, fields
from datetime import datetime


class PolishTest(models.Model):
    _name = "polish.test"
    _description ="Polish Test"
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string='Name', required=True)
    age = fields.Integer(string='Age')
    gender = fields.Selection([
        ('male', "Male"),
        ("female", "Female"),
        ("other", "other"),
    ], required=True, default='male')
    note = fields.Text(string="Description")
    date = fields.Date('Date', required=True, default=fields.Date.context_today)
    amount = fields.Float('Amount', required=True)
    active = fields.Boolean(default=True)
    color = fields.Integer(string='Color Index')
    respartner_id = fields.Many2one("res.partner", string="Responsible partner")
    resuser_id = fields.Many2many('res.users', string='Responsible user')










