# __manifest__.py
{
    'name': 'aadded Module',
    'version': '1.0',
    'author': 'kleinlo',
    'category': 'Uncategorized',
    'depends': ['base'],  # Add any dependencies here
    'data': [
        'views/create_folder_wizard_views.xml',
    ],
    'installable': True,
    'auto_install': False,
}