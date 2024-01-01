# models/create_folder_wizard.py
import os
from odoo import models, fields, api

class CreateFolderWizard(models.TransientModel):
    _name = 'create.folder.wizard'
    _description = 'Create Folder Wizard'

    folder_path = fields.Char(string='Folder Path', required=True)

    @api.multi
    def button_create_folder(self):
        for record in self:
            folder_name = f"OrderLine_{record._context.get('order_line_id')}"
            folder_path = os.path.join(record.folder_path, folder_name)

            if not os.path.exists(folder_path):
                os.makedirs(folder_path)

        return {'type': 'ir.actions.act_window_close'}