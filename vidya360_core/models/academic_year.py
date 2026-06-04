from odoo import models, fields, api

class AcademicYear(models.Model):
    _name = 'vidya.academic.year'
    _description = 'Academic Year'
    _order = 'start_date desc'

    name = fields.Char(string='Year Name', required=True, help="e.g., 2024-2025")
    start_date = fields.Date(string='Start Date', required=True)
    end_date = fields.Date(string='End Date', required=True)
    active = fields.Boolean(default=True)
    is_current = fields.Boolean(string='Current Year', default=False)
    term_ids = fields.One2many('vidya.academic.term', 'year_id', string='Terms')

    @api.constrains('is_current')
    def _check_single_current_year(self):
        for record in self:
            if record.is_current:
                other_currents = self.search([('id', '!=', record.id), ('is_current', '=', True)])
                if other_currents:
                    other_currents.write({'is_current': False})
