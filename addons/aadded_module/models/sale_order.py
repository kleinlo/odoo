# models/sale_order.py
from odoo import models, api

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    @api.multi
    def action_confirm(self):
        res = super(SaleOrder, self).action_confirm()

        for order in self:
            for order_line in order.order_line:
                create_folder_wizard = self.env['create.folder.wizard'].create({'folder_path': '/path/to/your/default/folder'})
                create_folder_wizard._context['order_line_id'] = order_line.id
                return {
                    'name': 'Create Folder',
                    'type': 'ir.actions.act_window',
                    'res_model': 'create.folder.wizard',
                    'view_mode': 'form',
                    'view_id': self.env.ref('custom_module.create_folder_wizard_form_view').id,
                    'target': 'new',
                    'context': self.env.context,
                }

        return res