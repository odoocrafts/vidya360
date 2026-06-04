from odoo import models, fields

class FeeGroup(models.Model):
    _name = 'vidya.fee.group'
    _description = 'Fee Group'
    _order = 'sequence, name'

    name = fields.Char(string='Fee Name', required=True, help="e.g., Tuition Fee, Transport Fee")
    description = fields.Text(string='Description')
    sequence = fields.Integer(string='Sequence', default=10)
    active = fields.Boolean(default=True)
