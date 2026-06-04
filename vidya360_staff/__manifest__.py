{
    'name': 'Vidya 360 Staff Management',
    'version': '19.0.1.0.0',
    'summary': 'Staff and Teacher management module for Vidya 360',
    'description': 'Manage educational staff, teachers, subjects, and non-teaching duties by extending standard HR.',
    'category': 'Education',
    'author': 'Vidya 360',
    'depends': ['vidya360_core', 'hr', 'hr_recruitment'],
    'data': [
        'views/hr_employee_views.xml',
        'views/section_views.xml',
    ],
    'installable': True,
    'application': True,
    'license': 'LGPL-3',
}
