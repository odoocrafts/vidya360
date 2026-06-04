from odoo import models, fields

class Room(models.Model):
    _name = 'vidya.room'
    _description = 'Room / Lab'
    _order = 'name'

    name = fields.Char(string='Room Name/Number', required=True)
    room_type = fields.Selection([
        ('classroom', 'Classroom'),
        ('lab', 'Laboratory'),
        ('library', 'Library'),
        ('hall', 'Hall/Auditorium'),
        ('other', 'Other')
    ], string='Room Type', default='classroom', required=True)
    capacity = fields.Integer(string='Capacity', default=30)
    active = fields.Boolean(default=True)
