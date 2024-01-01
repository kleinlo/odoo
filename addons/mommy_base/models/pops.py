#!/usr/bin/python3
# @Time    : 2022-09-22
# @Author  : Kevin Kong (kfx2007@163.com)

from odoo import api, fields, models, _
import logging

_logger = logging.getLogger(__name__)

POPUP_ACTION = '_action_pops_up_confirm'

class message_pops_up(models.TransientModel):
    _name = "mommy.message.popsup"
    _description="mommy message"

    name = fields.Char("Title")
    content = fields.Char("Message Content",readonly=True, default="This is a default message, using _action_pops_up_confirm of context model method to replace.")

    @api.model
    def get_action(self):
        form_view_id = self.env.ref('mommy_base.customize_window_form_view').id
        return {
            'name':self.name,
            'type':'ir.actions.act_window',
            'res_model':'mommy.message.popsup',
            'view_mode':'form',
            'target':'new',
            'res_id':self.id,
            'views':[(form_view_id,'form'),],
            'context':self._context
        }

    @api.model
    def get_confirm_action(self):
        form_view_id = self.env.ref('mommy_base.view_pops_up_confirm_form').id
        return {
            'name':self.name,
            'type':'ir.actions.act_window',
            'res_model':'mommy.message.popsup',
            'view_mode':'form',
            'target':'new',
            'res_id':self.id,
            'views':[(form_view_id,'form'),],
            'context':self._context
        }

    def btn_OK(self):
        return {
            'type':'ir.actions.act_window_close'
        }

    def button_confirm(self):
        """
        confirm action

        NOTE: there are two conditions:
        1. popsup depends on active records so we need active records setup.
        2. model method without records, in this case, just call model method.
        """
        call_back_func = self._context.get("call_back", POPUP_ACTION)
        records = self.active_records if self.active_records and hasattr(self.active_records,POPUP_ACTION) else  self if self and hasattr(self, POPUP_ACTION) else None
        if records:
            return getattr(records, call_back_func)()
        else:
            if hasattr(self.active_model, call_back_func):
                return getattr(self.active_model, call_back_func)()
            else:
                _logger.warning(f"[MOMMY Base]we couldn't find any proper model which has call function: {call_back_func}")