{
    'name': 'Vidya 360 Noticeboard & Events',
    'version': '1.0',
    'category': 'Education',
    'summary': 'Manage School Announcements and Events',
    'description': 'Noticeboard and Events management for Vidya 360',
    'author': 'Vidya 360',
    'depends': ['vidya360_core', 'mail'],
    'data': [
        'security/ir.model.access.csv',
        'views/vidya_notice_views.xml',
        'views/vidya_event_views.xml',
        'views/menu_views.xml',
    ],
    'installable': True,
    'application': True,
    'license': 'LGPL-3',
}
