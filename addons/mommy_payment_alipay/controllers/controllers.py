# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request
import logging
from odoo.exceptions import ValidationError

_logger = logging.getLogger(__name__)


class Alipay(http.Controller):

    @http.route('/payment/alipay/validate', type="http", auth="none", methods=['POST', 'GET'], csrf=False)
    def alipay_validate(self, **kwargs):
        """Validate Payment Result"""
        _logger.info("[Mommy Alipay]:Validate Payment Result...")
        try:
            _logger.debug(f"[Mommy Alipay]Result from alipay:{kwargs}")
            tx_obj  = request.env['payment.transaction'].sudo()
            tx = tx_obj._get_tx_from_notification_data('alipay', kwargs)
            tx._handle_notification_data('alipay', kwargs)
        except ValidationError:
            _logger.exception("[Mommy Alipay] Payment Exception")
        return request.redirect('/payment/status')

    @http.route('/payment/alipay/notify', csrf=False, type="http", auth='none', method=["POST"])
    def alipay_notify(self, **kwargs):
        """接收支付宝异步通知"""
        _logger.debug(f"接收支付宝异步通知...收到的数据:{kwargs}")
        """
        {
            'gmt_create': '2019-11-06 12:52:18', 
            'charset': 'utf-8', 
            'gmt_payment': '2019-11-06 12:52:28', 
            'notify_time': '2019-11-06 12:52:29', 
            'subject': 'SO015-1', 
            'sign': 'cG6uWeaX+5FXAJu7O02CI6b8V5L5Qamo/lz3LWvBVNCni4A5G1oWezCOVsqCEII/jO9mErQoY5ZXIW7uayRDOmp4nVWjl9kppDCNdi0YJHTdvY3WfoEUwc6XbDplUWWn9U5X00CPnUIlYMbfWaFFmsW/PVzhECBP2V08iBvbi2pscykf5LtyskG6gorJjzkNUE/WoOw+LV3JR30U8IFbfys7m67HDYRMjbdfSIGVDxZUfNMbgQK0/P3DyDQ0PbmdiD8w/e8WHM29cocJ20jnu8j5ZXyngWw09R/VAAW+15IHWJ+26JLA+vV/IM4Hp+v7C/my0Q+fpQPTcg6QEM/d5w==', 'buyer_id': '2088102179514385', 'passback_params': 'return_url%3Dhttp%3A%2F%2Fproject.mixoo.cn%3A80%2Fpayment%2Falipay%2Fvalidate%26reference%3DSO015-1%26amount%3D1.0%26currency%3DCNY%26csrf_token%3D24cc66c330aed25a1bcc9ca07dfbf8fa568327d6o1573019530%26notify_url%3Dhttp%3A%2F%2Fproject.mixoo.cn%3A80%2Fpayment%2Falipay%2Fnotify', 
            'invoice_amount': '1.00', 
            'version': '1.0', 
            'notify_id': '2019110600222125229014381000618776', 
            'fund_bill_list': '[{"amount":"1.00","fundChannel":"ALIPAYACCOUNT"}]', 
            'notify_type': 'trade_status_sync', 
            'out_trade_no': 'SO015-1', 
            'total_amount': '1.00', 
            'trade_status': 'TRADE_SUCCESS', 
            'trade_no': '2019110622001414381000117218', 
            'auth_app_id': '2016101100664659', 
            'receipt_amount': '1.00', 
            'point_amount': '0.00', 
            'app_id': '2016101100664659', 
            'buyer_pay_amount': '1.00', 
            'sign_type': 'RSA2', 
            'seller_id': '2088102179155775'
            }
        """
        payment = request.env["payment.provider"].sudo().search(
            [('code', '=', 'alipay')], limit=1)
        result = payment._verify_pay(kwargs)
        return "success" if result else "failed"
