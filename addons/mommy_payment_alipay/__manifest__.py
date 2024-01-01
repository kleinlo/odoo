# -*- coding: utf-8 -*-
{
    'name': "Payment Alipay",

    'summary': """Payment Alipay/支付宝""",

    'description': """
        Payment Alipay
        支付宝中国大陆版本
    """,
    'author': "OdooMommy Network Technology",
    'website': "http://odoomommy.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/12.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'tools',
    'version': '17.0.1.0',

    # any module necessary for this one to work correctly
    'depends': ['payment', 'mommy_base'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/views.xml',
        'views/templates.xml',
        'security/data.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
    "external_dependencies":{
        "python":['alipay-sdk']
    },
    "application": True,
    'post_init_hook': 'post_init_hook',
    'uninstall_hook': 'uninstall_hook',
    "images":["static/src/image/alipay.png"],
    "price": "50",
    "currency": 'EUR',
    "application": True,
    'support': 'kfx2007@163.com',
    "license": "OPL-1",
}
