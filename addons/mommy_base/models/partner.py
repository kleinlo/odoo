#!/usr/bin/python3
# @Time    : 2023-09-22
# @Author  : Kevin Kong (kfx2007@163.com)

from odoo import api, fields, models, _


class res_partner(models.Model):
    _inherit = "res.partner"

    external_layout_id = fields.Many2one(
        "ir.ui.view", string="Document Template")
    external_report_header = fields.Html("Company Tagline")
    external_company_details = fields.Html("Company Details")
    external_report_footer = fields.Html("Footer")
