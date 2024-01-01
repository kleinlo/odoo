#!/usr/bin/python3
# @Time    : 2022-04-24
# @Author  : Kevin Kong (kfx2007@163.com)

import odoo
import json
import logging
try:
    from BytesIO import BytesIO
except ImportError:
    from io import BytesIO
import zipfile
from datetime import datetime
from odoo import http
from odoo.http import request
from odoo.http import content_disposition


class MommyBase(http.Controller):

    # @http.route('/mommy/get_quick_edit/')
    # def index(self, **kw):
    #     """wether use quick edit or not."""
    #     enable = bool(request.env['ir.config_parameter'].sudo(
    #     ).get_param("mommy.quick.edit", True))
    #     return json.dumps({"quick_edit": enable})

    @http.route('/attachment/download', type='http', auth="public")
    def download_attachments(self, res_model, res_ids):
        """
            下载所有的附件
        """
        res_ids = res_ids.split(',')
        attachment_obj = request.env['ir.attachment'].sudo()
        domain = [('res_model', '=', res_model), ('res_id', 'in', res_ids)]
        attachment_ids = attachment_obj.search(domain)

        file_dict = {}
        for attachment_id in attachment_ids:
            file_store = attachment_id.store_fname
            if file_store:
                file_name = attachment_id.name
                file_path = attachment_id._full_path(file_store)
                file_dict["%s:%s" % (file_store, file_name)] = dict(
                    path=file_path, name=file_name)
        zip_filename = datetime.now()
        zip_filename = "%s.zip" % zip_filename
        bitIO = BytesIO()
        zip_file = zipfile.ZipFile(bitIO, "w", zipfile.ZIP_DEFLATED)
        for file_info in file_dict.values():
            zip_file.write(file_info["path"], file_info["name"])
        zip_file.close()
        headers = [('Content-Type', 'application/x-zip-compressed'),
                   ('Content-Disposition', content_disposition(zip_filename))]
        return request.make_response(bitIO.getvalue(),
                                     headers=headers)