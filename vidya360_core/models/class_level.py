from odoo import models, fields

class ClassLevel(models.Model):
    _name = 'vidya.class.level'
    _description = 'Class / Standard'
    _order = 'sequence, id'

    name = fields.Char(string='Class Name', required=True, help="e.g., Class 1, Grade 10")
    sequence = fields.Integer(string='Sequence', default=10)
    section_ids = fields.One2many('vidya.section', 'class_id', string='Sections')
    subject_ids = fields.Many2many('vidya.subject', string='Allocated Subjects')
    active = fields.Boolean(default=True)
