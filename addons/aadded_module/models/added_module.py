from odoo import models, fields

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    custom_many2many_field = fields.Many2many(
        'contract.year',  # Replace 'contract.year' with your actual model name
        string='Custom Many2many Field',
    )
