from odoo import models, fields

class StudentAttendance(models.Model):
    _name = 'vidya.attendance'
    _description = 'Student Attendance Record'

    student_id = fields.Many2one('vidya.student', string='Student', required=True)
    date = fields.Date(string='Date', required=True, default=fields.Date.context_today)
    status = fields.Selection([
        ('present', 'Present'),
        ('absent', 'Absent'),
        ('half_day', 'Half Day'),
        ('leave', 'Leave')
    ], string='Status', required=True, default='present')
    remarks = fields.Char(string='Remarks')
    sheet_id = fields.Many2one('vidya.attendance.sheet', string='Attendance Sheet', ondelete='cascade')

    _sql_constraints = [
        ('unique_student_date', 'unique(student_id, date)', 'A student can only have one attendance record per day!')
    ]
