from odoo import models, fields, api

class AttendanceSheet(models.Model):
    _name = 'vidya.attendance.sheet'
    _description = 'Class Attendance Sheet'

    name = fields.Char(string='Reference', compute='_compute_name')
    class_id = fields.Many2one('vidya.class.level', string='Class', required=True)
    section_id = fields.Many2one('vidya.section', string='Section', required=True, domain="[('class_id', '=', class_id)]")
    date = fields.Date(string='Date', required=True, default=fields.Date.context_today)
    state = fields.Selection([
        ('draft', 'Draft'),
        ('done', 'Submitted')
    ], string='State', default='draft')
    attendance_ids = fields.One2many('vidya.attendance', 'sheet_id', string='Attendances')

    @api.depends('section_id', 'date')
    def _compute_name(self):
        for sheet in self:
            if sheet.section_id and sheet.date:
                sheet.name = f"{sheet.section_id.class_id.name} {sheet.section_id.name} - {sheet.date}"
            else:
                sheet.name = "New Sheet"

    def action_load_students(self):
        self.ensure_one()
        students = self.env['vidya.student'].search([
            ('section_id', '=', self.section_id.id),
            ('active', '=', True)
        ])
        
        # Keep existing records for today
        existing_student_ids = self.attendance_ids.mapped('student_id').ids
        
        vals_list = []
        for student in students:
            if student.id not in existing_student_ids:
                vals_list.append((0, 0, {
                    'student_id': student.id,
                    'date': self.date,
                    'status': 'present'
                }))
        
        if vals_list:
            self.write({'attendance_ids': vals_list})

    def action_submit(self):
        self.write({'state': 'done'})
