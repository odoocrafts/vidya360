{
    'name': 'Vidya 360 Student Information System',
    'version': '19.0.1.0.0',
    'summary': 'Student management module for Vidya 360',
    'description': 'Manage student profiles, documents, and academic history.',
    'category': 'Education',
    'author': 'Vidya 360',
    'depends': ['vidya360_core'],
    'data': [
        'security/ir.model.access.csv',
        'data/ir_sequence_data.xml',
        'views/student_views.xml',
        'views/menu_views.xml',
    ],
    'installable': True,
    'application': True,
    'license': 'LGPL-3',
}
