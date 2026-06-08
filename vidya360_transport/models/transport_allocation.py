from odoo import models, fields, api, _

class TransportAllocation(models.Model):
    _name = 'vidya.transport.allocation'
    _description = 'Transport Allocation'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string="Reference", required=True, copy=False, readonly=True, default=lambda self: _('New'))
    occupant_type = fields.Selection([
        ('student', 'Student'),
        ('staff', 'Staff')
    ], string="Occupant Type", required=True, default='student')
    
    student_id = fields.Many2one('vidya.student', string="Student")
    staff_id = fields.Many2one('hr.employee', string="Staff")
    
    route_id = fields.Many2one('vidya.transport.route', string="Route", required=True)
    vehicle_id = fields.Many2one('vidya.transport.vehicle', string="Vehicle", required=True, domain="[('route_id', '=', route_id)]")
    
    start_date = fields.Date(string="Start Date", required=True, default=fields.Date.context_today)
    state = fields.Selection([
        ('draft', 'Draft'),
        ('active', 'Active'),
        ('cancelled', 'Cancelled')
    ], string="Status", default='draft', tracking=True)

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', _('New')) == _('New'):
                vals['name'] = self.env['ir.sequence'].next_by_code('vidya.transport.allocation') or _('New')
        return super().create(vals_list)

    def action_activate(self):
        self.write({'state': 'active'})

    def action_cancel(self):
        self.write({'state': 'cancelled'})
