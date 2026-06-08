from odoo import models, fields

class TransportVehicle(models.Model):
    _name = 'vidya.transport.vehicle'
    _description = 'Transport Vehicle'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string="License Plate", required=True, tracking=True)
    vehicle_model = fields.Char(string="Vehicle Model")
    driver_name = fields.Char(string="Driver Name", required=True)
    driver_phone = fields.Char(string="Driver Phone")
    capacity = fields.Integer(string="Capacity", required=True)
    route_id = fields.Many2one('vidya.transport.route', string="Assigned Route")
    active = fields.Boolean(default=True)
