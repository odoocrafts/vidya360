{
    'name': 'Vidya 360 Fee Management',
    'version': '19.0.1.0.0',
    'summary': 'Manage student fees, structures, discounts, and invoices.',
    'description': 'Automates fee generation and integrates with standard Odoo accounting for Vidya 360.',
    'category': 'Education',
    'author': 'Vidya 360',
    'depends': ['vidya360_core', 'vidya360_student', 'account'],
    'data': [
        'security/ir.model.access.csv',
        'wizards/generate_fee_invoice_views.xml',
        'views/menu_views.xml',
        'views/fee_structure_views.xml',
        'views/student_views.xml',
    ],
    'installable': True,
    'application': True,
    'license': 'LGPL-3',
}
