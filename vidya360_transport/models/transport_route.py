from odoo import models, fields

class TransportRoute(models.Model):
    _name = 'vidya.transport.route'
    _description = 'Transport Route'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string="Route Name", required=True, tracking=True)
    start_point = fields.Char(string="Start Point", required=True)
    end_point = fields.Char(string="End Point", required=True)
    distance = fields.Float(string="Distance (km)")
    active = fields.Boolean(default=True)
    notes = fields.Text(string="Notes")
