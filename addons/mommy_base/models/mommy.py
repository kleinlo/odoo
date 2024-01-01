#!/usr/bin/python3
# @Time    : 2022-04-24
# @Author  : Kevin Kong (kfx2007@163.com)

from odoo import api, fields, models, _


class mommy_base(models.AbstractModel):
    _name = "mommy.base"
    _description="Odoo Mommy Settings"

    @api.model
    def get_quick_edit(self):
        """wether using quick edit or not."""
        quick_edit = self.env['ir.config_parameter'].sudo(
        ).get_param("mommy.quick.edit","True")
        enable = quick_edit == 'True'
        return {"quick_edit": enable}
