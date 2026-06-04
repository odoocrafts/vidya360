{
    'name': 'Vidya 360 Admissions CRM',
    'version': '19.0.1.0.0',
    'summary': 'Manage student enquiries and admissions',
    'category': 'Education',
    'author': 'Vidya 360',
    'depends': ['crm', 'vidya360_student'],
    'data': [
        'security/ir.model.access.csv',
        'data/crm_stage_data.xml',
        'views/crm_lead_views.xml',
        'views/menu_views.xml',
    ],
    'installable': True,
    'application': True,
    'license': 'LGPL-3',
}
