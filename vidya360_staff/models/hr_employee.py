from odoo import models, fields, api

class HrEmployee(models.Model):
    _inherit = 'hr.employee'

    vidya_staff_type = fields.Selection([
        ('principal', 'Principal'),
        ('teacher', 'Teacher'),
        ('admin', 'Admin/Management'),
        ('office', 'Office Staff'),
        ('support', 'Support Staff'),
        ('driver', 'Driver')
    ], string='Staff Type', tracking=True)

    is_teacher = fields.Boolean(
        string='Is Teacher', 
        compute='_compute_is_teacher', 
        store=True
    )

    qualified_subject_ids = fields.Many2many(
        'vidya.subject', 
        string='Qualified Subjects',
        help="Subjects this teacher is qualified to teach."
    )

    duty_assignments = fields.Html(
        string='Duty Assignments',
        help="Specific duties assigned to non-teaching staff (e.g., Gate Duty, Library)."
    )

    @api.depends('vidya_staff_type')
    def _compute_is_teacher(self):
        for employee in self:
            employee.is_teacher = (employee.vidya_staff_type == 'teacher')
