#!/usr/bin/python3
# @Time    : 2022-10-08
# @Author  : Kevin Kong (kfx2007@163.com)

from odoo import api, fields, models, _
from odoo.addons.base.models.ir_property import TYPE2FIELD, TYPE2CLEAN
from autils.date import dateutil

TYPE2FIELD.update({
    'html': 'value_text',
})


TYPE2CLEAN.update({
    'html': lambda val: val or False,
})

RANGE_TYPES = [
    ('year', 'Year'),
    ('month', 'Month'),
    ('week', 'Week')
]


class ir_model(models.Model):
    _inherit = "ir.model"

    track = fields.Boolean(
        'Track All', help='Track all fields changes and displaying on chatter?')
    filter_read = fields.Boolean("Filter Read", default=False)


class ir_property(models.Model):

    _inherit = "ir.property"

    type = fields.Selection(selection_add=[('html', 'Html')], ondelete={
                            "html": "set default"})

    def get_by_record(self):
        self.ensure_one()
        if self.type in ('char', 'text', 'selection', 'html'):
            return self.value_text
        elif self.type == 'float':
            return self.value_float
        elif self.type == 'boolean':
            return bool(self.value_integer)
        elif self.type == 'integer':
            return self.value_integer
        elif self.type == 'binary':
            return self.value_binary
        elif self.type == 'many2one':
            if not self.value_reference:
                return False
            model, resource_id = self.value_reference.split(',')
            return self.env[model].browse(int(resource_id)).exists()
        elif self.type == 'datetime':
            return self.value_datetime
        elif self.type == 'date':
            if not self.value_datetime:
                return False
            return fields.Date.to_string(fields.Datetime.from_string(self.value_datetime))
        return False


class ir_sequence(models.Model):
    _inherit = "ir.sequence"

    def _create_date_range_by_type(self,dt):
        if self.range_type == 'year':
            date_from, date_to = date(dt.year,1,1), date(dt.year,12,31)
        if self.range_type == 'month':
            date_from, date_to = dateutil.get_first_and_last_day(dt.year, dt.month)
        else:
            date_from, date_to = dateutil.get_week_range(dt)

        seq_date_range = self.env['ir.sequence.date_range'].sudo().create({
            "date_from": date_from,
            "date_to": date_to,
            "sequence_id": self.id
        })
        return seq_date_range

    def _next(self, sequence_date=None):
        if not self.use_date_range:
            return super()._next(sequence_date)
        dt = sequence_date or self._context.get('ir_sequence_date', fields.Date.today())
        domain =[('sequence_id', '=', self.id), ('date_from', '<=', dt), ('date_to', '>=', dt)]
        seq_date = self.env['ir.sequence.date_range'].search(domain, limit=1)
        if not seq_date:
            seq_date = self._create_date_range_by_type(dt)
        return seq_date._next()

    range_type = fields.Selection(
        RANGE_TYPES, string="Subsequence Range", default="year", copy=False)