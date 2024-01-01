#!/usr/bin/python3
# @Time    : 2022-03-30
# @Author  : Kevin Kong (kfx2007@163.com)

from odoo import api, fields, models, _
from odoo.models import INSERT_BATCH_SIZE
from odoo.tools import split_every
from odoo.exceptions import UserError


class BaseModel(models.AbstractModel):

    _inherit = "base"

    def _pre_report_action(self):
        pass

    @property
    def active_model(self):
        active_model = self._context.get("active_model")
        return self.env[self._context.get("active_model")] if active_model else None

    @property
    def active_records(self):
        active_model, active_id, active_ids = self._context.get(
            "active_model"), self._context.get("active_id"), self._context.get("active_ids")
        if not active_model:
            return None
        if active_ids:
            return self.env[active_model].browse(active_ids)
        if active_id:
            return self.env[active_model].browse(active_id)

    def show_message(self, title, content):
        popsup = self.env['mommy.message.popsup'].create({
            "name": title,
            "content": content
        })
        return popsup.get_action()

    def show_confirm_message(self, title, content):
        confirm_pops_up = self.env['mommy.message.popsup'].create({
            "name": title,
            "content": content
        })
        return confirm_pops_up.get_confirm_action()

    def get_view_action(self, action_id=None, view_id=None, view_mode=None):
        """get view action"""
        model, res_ids = self._name, self.ids
        _logger.info(
            "[Mommy Base] opening model:%s res_ids:%s view action." % (model, res_ids))

        if not action_id:
            domain = [('res_model', '=', model)]
            action_id = self.env['ir.actions.act_window'].search(
                domain, limit=1)
            if not action_id:
                raise UserError(
                    _("Model: %s has no valid action for this operation." % model))

            if not view_mode:
                if len(res_ids) == 1:
                    mode = 'form'
                else:
                    mode = 'tree'
            else:
                mode = view_mode

            if not view_id:
                domain = [('model', '=', model), ('type', '=', mode)]
                view_id = self.env['ir.ui.view'].search(domain, limit=1)
            else:
                view_id = self.env.ref(view_id).id
            action = action_id.read()[0]
            action['views'] = [(view_id.id, mode)]
        else:
            action = action_id.read()[0]

        if mode == 'form':
            action['res_id'] = res_ids[0]
        else:
            action['domain'] = [('id', 'in', res_ids)]
        return action

    def get_selection_desc(self, field):
        return dict(self._fields[field]._description_selection(self.env)).get(getattr(self, field))

    def get_all_attachments(self):
        """
            get all attachments related to this record.
        """
        domain = [('res_model', '=', self._name), ('res_id', '=', self.id)]
        return self.env['ir.attachment'].sudo().search(domain)

    def get_report_header(self):
        """
        get objects report headers
        """
        if 'partner_id' in self and self.partner_id \
            and 'external_report_header' in self.partner_id and self.partner_id.external_report_header:
            return self.partner_id.external_report_header
        return self.env.company.report_header

    def get_report_details(self):
        if 'partner_id' in self and self.partner_id \
            and 'external_company_details' in self.partner_id and self.partner_id.external_company_details:
            return self.partner_id.external_company_details
        return self.env.company.company_details

    def get_report_footer(self):
        if 'partner_id' in self and self.partner_id \
            and 'external_report_footer' in self.partner_id and self.partner_id.external_report_footer:
            return self.partner_id.external_report_footer
        return self.env.company.report_footer
