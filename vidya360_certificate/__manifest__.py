{
    'name': 'Vidya 360 Certificates',
    'version': '19.0.1.0.0',
    'summary': 'Generate and manage student certificates.',
    'description': 'Dynamic certificate engine for Vidya 360.',
    'category': 'Education',
    'author': 'Vidya 360',
    'depends': ['vidya360_core', 'vidya360_student'],
    'data': [
        'security/ir.model.access.csv',
        'reports/certificate_report.xml',
        'views/certificate_request_views.xml',
        'views/menu_views.xml',
    ],
    'installable': True,
    'application': True,
    'license': 'LGPL-3',
}
