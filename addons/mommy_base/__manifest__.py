# -*- coding: utf-8 -*-
{
    'name': "Mommy Base",

    'summary': """
        Basic feature powered by Odoomommy.com
    """,

    'description': """
        *1. 支持指定计算字段分组汇总
        2. 控制个人编辑区域显示效果 
        3. 设置系统标题
        *4. 封装统一提示框和统一确认框
        *5. 表单设置每页条目数量
        *6. 集成模型字段跟踪功能
        *7. 集成快速设置单据号码方法
        *8. 设置字段标签颜色
        *9. 报表支持打印前校验
        *10. 新增表单动作视图快速获取方法的方法
        *11. 添加字段唯一性校验，支持定制提示文字
        *12. 登录页面屏蔽数据库管理链接&Powered by Odoo
        *13. 添加获取字段描述方法
        *14. 添加获取当前记录所有关联附件的方法
        *15. company_dependent属性添加对Html字段的支持。
        *16. 过滤读取功能
    """,

    'author': "OdooMommy",
    'website': "http://www.odoomommy.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/13.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'basic',
    'version': '17.0.1.0',

    # any module necessary for this one to work correctly
    'depends': ['sale'],

    # always loaded
    'data': [
        'security/data.xml',
        'security/payment_method.xml',
        'security/payment_provider.xml',
        'security/ir.model.access.csv',
        'views/views.xml',
        'views/templates.xml',
        'views/settings.xml',
        'views/pops.xml',
        'views/ir.xml',
        'views/mail_template.xml',
        'views/layout.xml',
        'views/partner.xml'
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
    "external_dependencies":{
        "python":['wechatpy']
    },
    "price":"30",
    "currency":"EUR",
    "assets": {
        "web.assets_backend":[
            "mommy_base/static/src/js/mommy.js"
        ],
        "web.assets_qweb":[
            "mommy_base/static/srx/xml/*"
        ]
    }
}
