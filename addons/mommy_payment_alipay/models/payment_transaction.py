#!/usr/bin/python3
# @Time    : 2023-09-19
# @Author  : Kevin Kong (kfx2007@163.com)

from xml import dom
from odoo import api, fields, models, _
from odoo.exceptions import ValidationError
import logging

_logger = logging.getLogger(__name__)


class TxAlipay(models.Model):
    _inherit = 'payment.transaction'

    def _get_specific_rendering_values(self, processing_values):
        res = super()._get_specific_rendering_values(processing_values)
        if self.provider_code != 'alipay':
            return res
        
        api_url = self.provider_id._alipay_get_api_url(self.amount, self.reference)
        alipay_values = {
            "api_url": api_url,
        }

        return alipay_values

    alipay_txn_type = fields.Char('Aliapy Transaction type')

    def _get_tx_from_notification_data(self, provider_code, notification_data):
        """
        Override of payment to find the transaction based on Alipay data.
        """
        tx = super()._get_tx_from_notification_data(provider_code, notification_data)
        if provider_code != 'alipay' or len(tx) == 1:
            return tx
        
        reference = notification_data.get('out_trade_no')
        tx = self.search([('reference', '=', reference), ('provider_code', '=', 'alipay')])
        if not tx:
            raise ValidationError(
                "Alipay: " + _("No transaction found matching reference %s.", reference)
            )
        return tx
    

    def _process_notification_data(self, notification_data):
        """
        Override of payment to process the transaction based on Alipay data
        """
        super()._process_notification_data(notification_data)
        if self.provider_code != 'alipay':
            return
        
        if not notification_data:
            self._set_canceled(_("The customer left the payment page."))
            return
        
        # {'charset': 'utf-8', 'out_trade_no': 'S00001', 
        # 'method': 'alipay.trade.page.pay.return', 'total_amount': '1.00', 
        # 'sign': 'Z9hgmsv1IIO8fucWNglnNpiqpbzW6Iwrt4Xu8w4qxUqBtK+dFLk57gqxRbBaCAo2mrYm50sKRNpv/J72RtUHH6EMieK9Id6fnAQpqx5DqN+V/w52MESLPya0980dSL3Au9+7w2WkaS3ANYcYnpLiTJBUvQBtW7X0smV1RWs4iYGXBzd89bIwmDh2DSBFCe+LRtXLjtOvU8lKi5QiX3kbhom6dv7rim3pzQpFIx+ZBFgZENZAy0zMvDFgUkc5pnxALsCpa/pEtfz8G98yWATu8nib8cuwsEmCtuUNB5k916ExuTgXsjKc2t70Y9irqYxH8A29wscc99SMfey5vBZEGA==', 
        # 'trade_no': '2023120922001401390501567941', 'auth_app_id': '9021000128667504', 
        # 'version': '1.0', 'app_id': '9021000128667504', 
        # 'sign_type': 'RSA2', 'seller_id': '2088721014009864', 
        # 'timestamp': '2023-12-09 08:16:36'}
        
        print('++++alipay+++++')
        print(notification_data)

        # 根据支付宝同步返回的信息，去支付宝服务器查询
        domain = [('code', '=', 'alipay')]
        payment = self.env["payment.provider"].sudo().search(domain, limit=1)
        alipay = payment._get_alipay()
        res = alipay.pay.trade_query(out_trade_no=notification_data["out_trade_no"])
        # 校验结果
        if res["code"] == "10000" and res["trade_status"] in ("TRADE_SUCCESS", "TRADE_FINISHED"):
            _logger.info(f"支付单：{notification_data['out_trade_no']} 已成功付款")
            date_validate = fields.Datetime.now()
            res.update(date=date_validate)
            self._set_done()
        elif res["code"] == "10000" and res["trade_status"] == "WAIT_BUYER_PAY":
            _logger.info(f"支付单：{notification_data['out_trade_no']} 正等待付款...")
            self._set_pending()
        elif res["code"] == "10000" and res["trade_status"] == "TRADE_CLOSED":
            _logger.info(f"支付单：{notification_data['out_trade_no']} 已关闭或已退款.")
            self._set_canceled()
        else:
            _logger.info(
                "received data with invalid payment status (%s) for transaction with reference %s",
                res["trade_status"], notification_data["out_trade_no"],
            )
            self._set_error("Alipay: " + _("received invalid transaction status: %s", res["trade_status"]))