from odoo import models, fields

class AcademicTerm(models.Model):
    _name = 'vidya.academic.term'
    _description = 'Academic Term'
    _order = 'start_date'

    name = fields.Char(string='Term Name', required=True, help="e.g., Term 1, Semester 1")
    year_id = fields.Many2one('vidya.academic.year', string='Academic Year', required=True, ondelete='cascade')
    start_date = fields.Date(string='Start Date', required=True)
    end_date = fields.Date(string='End Date', required=True)
