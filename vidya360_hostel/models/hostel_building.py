from odoo import models, fields

class HostelBuilding(models.Model):
    _name = 'vidya.hostel.building'
    _description = 'Hostel Building'
    _order = 'name'

    name = fields.Char(string='Building Name', required=True)
    building_type = fields.Selection([
        ('boys', 'Boys Hostel'),
        ('girls', 'Girls Hostel'),
        ('general', 'General/Co-ed')
    ], string='Hostel Type', default='general', required=True)
    
    address = fields.Text(string='Address')
    warden_id = fields.Many2one('hr.employee', string='Warden')
    
    room_ids = fields.One2many('vidya.hostel.room', 'building_id', string='Rooms')
    
    total_capacity = fields.Integer(string='Total Capacity', compute='_compute_capacity', store=True)
    current_occupancy = fields.Integer(string='Current Occupancy', compute='_compute_capacity', store=True)
    
    active = fields.Boolean(default=True)

    def _compute_capacity(self):
        for building in self:
            building.total_capacity = sum(building.room_ids.mapped('capacity'))
            building.current_occupancy = sum(building.room_ids.mapped('current_occupancy'))
