from odoo import models, fields, api
from odoo.exceptions import ValidationError

class Timetable(models.Model):
    _name = 'vidya.timetable'
    _description = 'Class Timetable'
    _order = 'academic_year_id desc, class_id, section_id'

    name = fields.Char(string='Reference', required=True, copy=False, default='New')
    academic_year_id = fields.Many2one('vidya.academic.year', string='Academic Year', required=True)
    term_id = fields.Many2one('vidya.academic.term', string='Term', domain="[('year_id', '=', academic_year_id)]")
    class_id = fields.Many2one('vidya.class.level', string='Class', required=True)
    section_id = fields.Many2one('vidya.section', string='Section', required=True, domain="[('class_id', '=', class_id)]")
    state = fields.Selection([
        ('draft', 'Draft'),
        ('active', 'Active'),
        ('archived', 'Archived')
    ], string='Status', default='draft', tracking=True)
    
    line_ids = fields.One2many('vidya.timetable.line', 'timetable_id', string='Schedule Lines')

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', 'New') == 'New':
                # Simplified name generation
                vals['name'] = "Timetable"
        res = super().create(vals_list)
        for record in res:
            record.name = f"{record.academic_year_id.name} - {record.section_id.class_id.name} {record.section_id.name}"
        return res

class TimetableLine(models.Model):
    _name = 'vidya.timetable.line'
    _description = 'Timetable Line'
    _order = 'day_of_week, period_id'

    timetable_id = fields.Many2one('vidya.timetable', string='Timetable', required=True, ondelete='cascade')
    day_of_week = fields.Selection([
        ('0', 'Monday'),
        ('1', 'Tuesday'),
        ('2', 'Wednesday'),
        ('3', 'Thursday'),
        ('4', 'Friday'),
        ('5', 'Saturday'),
        ('6', 'Sunday')
    ], string='Day', required=True)
    period_id = fields.Many2one('vidya.period', string='Period', required=True)
    subject_id = fields.Many2one('vidya.subject', string='Subject', required=True)
    teacher_id = fields.Many2one('hr.employee', string='Teacher', domain="[('is_teacher', '=', True)]", required=True)
    room_id = fields.Many2one('vidya.room', string='Room')

    # SQL Constraints for Double Booking
    _sql_constraints = [
        ('unique_teacher_slot', 
         'UNIQUE(day_of_week, period_id, teacher_id)', 
         'This teacher is already assigned to a class during this period!'),
        ('unique_room_slot', 
         'UNIQUE(day_of_week, period_id, room_id)', 
         'This room is already occupied during this period!'),
        ('unique_section_slot',
         'UNIQUE(timetable_id, day_of_week, period_id)',
         'This section already has a class scheduled for this period!')
    ]
