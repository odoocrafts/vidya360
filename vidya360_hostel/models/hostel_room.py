from odoo import models, fields, api
from odoo.exceptions import ValidationError

class HostelRoom(models.Model):
    _name = 'vidya.hostel.room'
    _description = 'Hostel Room'
    _order = 'name'

    name = fields.Char(string='Room Number/Name', required=True)
    building_id = fields.Many2one('vidya.hostel.building', string='Hostel Building', required=True)
    
    category = fields.Selection([
        ('single', 'Single Room'),
        ('double', 'Double Room'),
        ('shared', 'Shared Room')
    ], string='Room Category', default='shared', required=True)
    
    room_type = fields.Selection([
        ('ac', 'AC'),
        ('non_ac', 'Non-AC')
    ], string='Room Type', default='non_ac')
    
    capacity = fields.Integer(string='Capacity (Beds)', required=True, default=2)
    current_occupancy = fields.Integer(string='Current Occupancy', compute='_compute_occupancy', store=True)
    available_beds = fields.Integer(string='Available Beds', compute='_compute_occupancy', store=True)
    
    rent_amount = fields.Monetary(string='Rent / Cost per Term', currency_field='currency_id')
    currency_id = fields.Many2one('res.currency', string='Currency', default=lambda self: self.env.company.currency_id)
    
    allocation_ids = fields.One2many('vidya.hostel.allocation', 'room_id', string='Allocations')
    company_id = fields.Many2one('res.company', string='Company', default=lambda self: self.env.company)
    
    active = fields.Boolean(default=True)

    @api.depends('capacity', 'allocation_ids.state')
    def _compute_occupancy(self):
        for room in self:
            active_allocations = len(room.allocation_ids.filtered(lambda a: a.state == 'allocated'))
            room.current_occupancy = active_allocations
            room.available_beds = room.capacity - active_allocations

    @api.constrains('capacity', 'current_occupancy')
    def _check_capacity(self):
        for room in self:
            if room.current_occupancy > room.capacity:
                raise ValidationError(f"Room {room.name} has exceeded its capacity! Cannot allocate more occupants than available beds.")
