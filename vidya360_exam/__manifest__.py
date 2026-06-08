{
    'name': 'Vidya 360 Exams & Results Management',
    'version': '1.0',
    'category': 'Education',
    'summary': 'Manage School Exams, Schedules, and Student Results',
    'description': 'Exams and Results Management for Vidya 360',
    'author': 'Vidya 360',
    'depends': ['base', 'mail', 'vidya360_core', 'vidya360_student'],
    'data': [
        'security/ir.model.access.csv',
        'views/exam_views.xml',
        'views/exam_schedule_views.xml',
        'views/exam_result_views.xml',
        'views/menu_views.xml',
    ],
    'installable': True,
    'application': True,
    'license': 'LGPL-3',
}
