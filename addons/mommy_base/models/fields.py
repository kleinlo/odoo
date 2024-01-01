#!/usr/bin/python3
# @Time    : 2022-11-16
# @Author  : Kevin Kong (kfx2007@163.com)

import odoo
from odoo.exceptions import UserError

class Field(odoo.fields.Field):

    unique = False
    exception = None

odoo.fields._String.__bases__ = (Field,)
