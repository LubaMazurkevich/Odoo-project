from odoo import models, fields , api
from datetime import datetime


class PolishTest(models.Model):
    _name = "polish.test"
    _description ="Polish Test"
    # _inherit = ['mail.thread', 'mail.activity.mixin']
    #
    # name = fields.Char(string='Name', required=True)
    # age = fields.Integer(string='Age')
    # gender = fields.Selection([
    #     ("male", "Male"),
    #     ("female", "Female"),
    #     ("other", "other"),
    # ], required=True, default='male')
    # note = fields.Text(string="Description")
    # date = fields.Date('Date', required=True, default=fields.Date.context_today)
    # amount = fields.Float('Amount', required=True)
    # active = fields.Boolean(default=True)
    # color = fields.Integer(string='Color Index')
    # respartner_id = fields.Many2one(comodel_name="res.partner", string="Responsible partner")
    # resuser_id = fields.Many2many('res.users', string='Responsible user')
    # polish_test_ids = fields.One2many(comodel_name="polish", inverse_name='test_id', string="polish")

    text = fields.Text(string="Text")
    select1 = fields.Selection([
            ("1", "1"),
            ("2", "2"),
            ("3", "3"),
    ], required=True, default='1')
    select2 = fields.Selection([
            ("4", "4"),
            ("5", "5"),
            ("6", "6"),
    ], required=True, default='4')
    boolean1 = fields.Boolean(string="1")
    boolean2 = fields.Boolean(string="2")
    boolean3 = fields.Boolean(string="3")
    boolean4 = fields.Boolean(string="4")
    boolean5 = fields.Boolean(string="5")
    boolean6 = fields.Boolean(string="6")
    boolean7 = fields.Boolean(string="7")
    boolean8 = fields.Boolean(string="8")
    boolean9 = fields.Boolean(string="9")

    check1 = fields.Boolean(string="Test 1")
    check2 = fields.Boolean(string="Test 2")
    check_all = fields.Boolean(string="Select all")

    # vehicle_type = fields.Selection(related='model_id.vehicle_type')

    class Polish(models.Model):
        _name = "polish"
        _description = "Polish"

        test_id = fields.Many2one(comodel_name="polish.test", string="Test")
        name = fields.Char(string="Name")

    @api.onchange('check_all')
    def _onchange_check_all(self):
        if self.check_all:
            self.check1 = True
            self.check2 = True
        else:
            self.check1 = False
            self.check2 = False

    # @api.onchange('check1')
    # def _onchange_check_all(self):
    #     if self.check1:
    #
    #     else:









