from odoo import models, fields

class VidyaExam(models.Model):
    _name = 'vidya.exam'
    _description = 'Examination Period'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string="Exam Name", required=True, tracking=True)
    academic_year_id = fields.Many2one('vidya.academic.year', string="Academic Year", required=True)
    term_id = fields.Many2one('vidya.academic.term', string="Term", domain="[('year_id', '=', academic_year_id)]")
    
    start_date = fields.Date(string="Start Date", required=True)
    end_date = fields.Date(string="End Date", required=True)
    
    state = fields.Selection([
        ('draft', 'Draft'),
        ('scheduled', 'Scheduled'),
        ('ongoing', 'Ongoing'),
        ('completed', 'Completed')
    ], string="Status", default='draft', tracking=True)

    def action_schedule(self):
        self.write({'state': 'scheduled'})

    def action_ongoing(self):
        self.write({'state': 'ongoing'})

    def action_complete(self):
        self.write({'state': 'completed'})
