from odoo import models, fields , api


class PolishTest(models.Model):

    _name = "polish.test"
    _description = "Polish Test"
    text = fields.Text(string="Text")
    select1 = fields.Selection([
            ("1", "1"),
            ("2", "2"),
            ("3", "3"),
    ], required=True, default="1")
    select2 = fields.Selection([
            ("4", "4"),
            ("5", "5"),
            ("6", "6"),
    ], required=True, default="4")
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

    @api.onchange("check_all")
    def _onchange_check_all(self):
        if self.check_all:
            self.check1 = True
            self.check2 = True
        else:
            self.check1 = False
            self.check2 = False

    @api.onchange("check1")
    def _onchange_check1_check2(self):
        if self.check1 and self.check2:
            self.text = f"[{self._fields['check2'].string}] { {self._fields['check1'].string} }"
        elif self.check1 and self.check2 != True:
            self.text = f"[{self._fields['check1'].string}]"
        elif self.check2 and self.check1 != True:
            self.text = {self._fields["check2"].string}
        else:
            self.text = " "

    @api.onchange("check2")
    def _onchange_check1_check2_(self):
        if self.check2 and self.check1:
            self.text = f"{ {self._fields['check1'].string} } [{self._fields['check2'].string}]"
        elif self.check1 and self.check2 != True:
            self.text = f"[{self._fields['check1'].string}]"
        elif self.check2 and self.check1 != True:
            self.text = {self._fields["check2"].string}
        else:
            self.text = " "

    def action_wiz_open(self):
        return {"type": "ir.actions.act_window",
                "res_model": "polish.update.text.wizard",
                "view_mode": "form",
                "target": "new"}














