from odoo import models, fields, api
from odoo.exceptions import UserError

class HostelAllocation(models.Model):
    _name = 'vidya.hostel.allocation'
    _description = 'Hostel Room Allocation'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'start_date desc'

    name = fields.Char(string='Reference', required=True, copy=False, readonly=True, default='New')
    
    occupant_type = fields.Selection([
        ('student', 'Student'),
        ('staff', 'Staff')
    ], string='Occupant Type', default='student', required=True, tracking=True)
    
    student_id = fields.Many2one('vidya.student', string='Student', tracking=True)
    staff_id = fields.Many2one('hr.employee', string='Staff', tracking=True)
    
    room_id = fields.Many2one('vidya.hostel.room', string='Room', required=True, tracking=True)
    building_id = fields.Many2one(related='room_id.building_id', string='Hostel', store=True)
    
    start_date = fields.Date(string='Start Date', default=fields.Date.context_today, required=True, tracking=True)
    end_date = fields.Date(string='End Date', tracking=True)
    
    state = fields.Selection([
        ('draft', 'Draft'),
        ('allocated', 'Allocated'),
        ('vacated', 'Vacated')
    ], string='Status', default='draft', required=True, tracking=True)
    
    company_id = fields.Many2one('res.company', string='Company', default=lambda self: self.env.company)

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', 'New') == 'New':
                vals['name'] = self.env['ir.sequence'].next_by_code('vidya.hostel.allocation') or 'New'
        return super().create(vals_list)

    def action_allocate(self):
        for record in self:
            if record.room_id.available_beds <= 0:
                raise UserError(f"Room {record.room_id.name} is fully occupied!")
            if record.occupant_type == 'student' and not record.student_id:
                raise UserError("Please select a student.")
            if record.occupant_type == 'staff' and not record.staff_id:
                raise UserError("Please select a staff member.")
            record.state = 'allocated'

    def action_vacate(self):
        for record in self:
            record.state = 'vacated'
            if not record.end_date:
                record.end_date = fields.Date.context_today(self)
