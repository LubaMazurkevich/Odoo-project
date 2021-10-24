from odoo import models, fields, api


class CreatePolishWizard(models.TransientModel):

    _name = "create.polish.wizard"
    _description = "Create Polish Wizard"

    text = fields.Text(string="Text")

    def update_polish_text(self):
        print("Button is clicked")
        self.env['polish.test'].browse(self._context.get('active_ids')).update({'text': self.text})
        return True

