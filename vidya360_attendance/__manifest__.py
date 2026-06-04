{
    'name': 'Vidya 360 Attendance',
    'version': '19.0.1.0.0',
    'summary': 'Manage daily student attendance',
    'category': 'Education',
    'author': 'Vidya 360',
    'depends': ['vidya360_student'],
    'data': [
        'security/ir.model.access.csv',
        'views/attendance_views.xml',
        'views/attendance_sheet_views.xml',
        'views/menu_views.xml',
    ],
    'installable': True,
    'application': True,
    'license': 'LGPL-3',
}
