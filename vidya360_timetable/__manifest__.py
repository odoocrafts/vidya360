{
    'name': 'Vidya 360 Timetable',
    'version': '19.0.1.0.0',
    'summary': 'Class and Teacher Timetable Management',
    'description': 'Schedule classes, manage periods, assign rooms, and prevent double-booking for Vidya 360.',
    'category': 'Education',
    'author': 'Vidya 360',
    'depends': ['vidya360_core', 'vidya360_staff'],
    'data': [
        'security/ir.model.access.csv',
        'views/menu_views.xml',
        'views/room_views.xml',
        'views/period_views.xml',
        'views/timetable_views.xml',
    ],
    'installable': True,
    'application': True,
    'license': 'LGPL-3',
}
