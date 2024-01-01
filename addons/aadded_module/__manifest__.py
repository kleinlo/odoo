# my_module/__manifest__.py

{
    'name': 'aadded module',
    'version': '1.0',
    'depends': ['sale'],  # Add dependencies if needed
    'data': [
        'views/sale_order_tree_inherit.xml',
        'views/sale_order_form_inherit.xml',
    ],
    'installable': True,
    'auto_install': False,
}
