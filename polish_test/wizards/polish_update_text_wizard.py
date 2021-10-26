from odoo import models, fields, api


class PolishUpdateTextWizard(models.TransientModel):

    _name = "polish.update.text.wizard"
    _description = "Create Polish Wizard"

    note = fields.Text(string="Note")

    def update_polish_text_wizard(self):
        self.env["polish.test"].browse(self._context.get("active_ids")).update({"note": self.note})

    def create_contact(self):
        self.env["res.partner"].create({"name": self.note})



