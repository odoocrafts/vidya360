from odoo import models, fields

class Section(models.Model):
    _inherit = 'vidya.section'

    class_teacher_id = fields.Many2one(
        'hr.employee', 
        string='Class Teacher', 
        domain="[('is_teacher', '=', True)]",
        help="Teacher assigned to this section."
    )
