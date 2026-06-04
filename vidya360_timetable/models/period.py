from odoo import models, fields

class Period(models.Model):
    _name = 'vidya.period'
    _description = 'Timetable Period'
    _order = 'sequence'

    name = fields.Char(string='Period Name', required=True, help="e.g., Period 1, Lunch Break")
    sequence = fields.Integer(string='Sequence', default=10)
    start_time = fields.Float(string='Start Time', required=True)
    end_time = fields.Float(string='End Time', required=True)
    is_break = fields.Boolean(string='Is Break', default=False)
    active = fields.Boolean(default=True)
