from odoo import models, fields

class EstateProperty(models.Model):
    _name = 'estate.property'
    _description = 'Estate Property'

    name = fields.Char(required=True)
    expected_price = fields.Float(required=True)
    selling_price = fields.Float(readonly=True, copy=False)
    availability_date = fields.Date()
    bedroom_number = fields.Integer(default=3)
    active = fields.Boolean('Active', default=True)