from odoo import models, fields

class Section(models.Model):
    _name = 'vidya.section'
    _description = 'Class Section'
    _order = 'class_id, name'

    name = fields.Char(string='Section Name', required=True, help="e.g., A, B, C")
    class_id = fields.Many2one('vidya.class.level', string='Class', required=True, ondelete='cascade')
    capacity = fields.Integer(string='Capacity', default=30)
