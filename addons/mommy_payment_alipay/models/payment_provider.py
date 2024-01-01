# -*- coding: utf-8 -*-

from odoo import models, fields, api
from alipay.api import AliPay, SANDBOX_URL, URL
from Crypto.PublicKey import RSA
import base64
from urllib.parse import quote_plus
from odoo.exceptions import ValidationError
import requests
from odoo.addons.mommy_payment_alipay import const
import logging

_logger = logging.getLogger(__name__)


class PaymentProvider(models.Model):
    _inherit = 'payment.provider'

    def _get_alipay(self):
        """
        Getting Alipay Client
        """
        try:
            private_key = RSA.importKey(base64.b64decode(
                self.alipay_secret).decode('utf-8'))
            public_key = RSA.importKey(base64.b64decode(
                self.alipay_public_key).decode('utf-8'))
            if self.state == "enabled":
                alipay = AliPay(self.alipay_appid, private_key, ali_public_key=public_key,
                                sign_type=self.alipay_sign_type)
            else:
                alipay = AliPay(self.alipay_appid, private_key, ali_public_key=public_key,
                                sign_type=self.alipay_sign_type, sandbox=True)
            return alipay
        except Exception as err:
            _logger.exception(
                "[Mommy Alipay]:Exception of generating alipay client.")

    def _alipay_get_api_url(self, amount, reference):
        """Alipay URL"""
        cfg_obj = self.env['ir.config_parameter'].sudo()
        base_url = cfg_obj.get_param('web.base.url')
        alipay = self._get_alipay()
        alipay.return_url = f'{base_url}/payment/alipay/validate'
        alipay.notify_url = f'{base_url}/payment/alipay/notify'
        url = alipay.pay.trade_page_pay(reference, amount,
                                        reference, product_code="FAST_INSTANT_TRADE_PAY")
        return url
    
    def _get_supported_currencies(self):
        """ Override of `payment` to return the supported currencies. """
        supported_currencies = super()._get_supported_currencies()
        if self.code == 'alipay':
            supported_currencies = supported_currencies.filtered(
                lambda c: c.name in const.SUPPORTED_CURRENCIES
            )
        return supported_currencies
    
    def _get_default_payment_method_codes(self):
        """ Override of `payment` to return the default payment method codes. """
        default_codes = super()._get_default_payment_method_codes()
        if self.code != 'alipay':
            return default_codes
        return const.DEFAULT_PAYMENT_METHODS_CODES

    code = fields.Selection(selection_add=[('alipay', "AliPay")], ondelete={
                            'alipay': 'set default'})
    seller_id = fields.Char("Alipay Seller Id")
    alipay_appid = fields.Char("Alipay AppId")
    alipay_secret = fields.Binary("Merchant Private Key")
    alipay_public_key = fields.Binary("Alipay Public Key")
    alipay_sign_type = fields.Selection(
        selection=[('rsa', 'RSA'), ('rsa2', 'RSA2')], string="Sign Type")

    # @api.model
    # def alipay_compute_fees(self, amount, currency_id, country_id):
    #     if not self.fees_active:
    #         return 0.0
    #     return self.fees_dom_var / 100 * amount
