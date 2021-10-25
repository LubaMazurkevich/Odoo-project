from odoo import models, fields, api


class PolishUpdateTextWizard(models.TransientModel):

    _name = "polish.update.text.wizard"
    _description = "Create Polish Wizard"

    text = fields.Text(string="Text")

    def update_polish_text_wizard(self):
        print("Button is clicked")
        self.env['polish.test'].browse(self._context.get('active_ids')).update({'text': self.text})
        return True



