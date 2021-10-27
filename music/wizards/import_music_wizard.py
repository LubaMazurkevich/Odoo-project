from odoo import models, fields


class ImportMusicWizard(models.TransientModel):

    _name = "import.music.wizard"
    _description = "Create Music Wizard"

    file = fields.Binary(string="File", required=True)

    def upload_file_wizard(self):
        print("Check")




