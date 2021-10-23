from odoo import models, fields, api


class CreatePolishWizard(models.TransientModel):

    _name = "create.polish.wizard"
    _description = "Create Polish Wizard"

    name = fields.Char(string='Name', required=True)
    polish_test_id= fields.Many2one('polish.test', string='Polish Test member', required=True)

    def action_create_polish(self):
        print("Button is clicked")
        return True

