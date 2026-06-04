from odoo import models, fields, api

class CertificateRequest(models.Model):
    _name = 'vidya.certificate.request'
    _description = 'Certificate Request'
    _order = 'date_request desc, id desc'

    name = fields.Char(string='Reference', required=True, copy=False, default='New')
    student_id = fields.Many2one('vidya.student', string='Student', required=True)
    certificate_type = fields.Selection([
        ('bonafide', 'Bonafide Certificate'),
        ('conduct', 'Conduct Certificate'),
        ('character', 'Character Certificate'),
        ('study', 'Study Certificate'),
        ('fee_paid', 'Fee Paid Certificate'),
        ('tc', 'Transfer Certificate'),
        ('course_completion', 'Course Completion Certificate')
    ], string='Certificate Type', required=True)
    
    date_request = fields.Date(string='Request Date', default=fields.Date.context_today, required=True)
    date_issue = fields.Date(string='Issue Date')
    purpose = fields.Char(string='Purpose')
    state = fields.Selection([
        ('draft', 'Draft'),
        ('approved', 'Approved'),
        ('issued', 'Issued'),
        ('rejected', 'Rejected')
    ], string='Status', default='draft', tracking=True)
    
    # Specific Fields for different certificates
    academic_year_id = fields.Many2one('vidya.academic.year', string='Academic Year')
    class_id = fields.Many2one('vidya.class.level', string='Class')
    
    character_evaluation = fields.Selection([
        ('excellent', 'Excellent'),
        ('good', 'Good'),
        ('satisfactory', 'Satisfactory')
    ], string='Evaluation')
    
    reason_for_leaving = fields.Char(string='Reason for Leaving')
    last_date_of_attendance = fields.Date(string='Last Date of Attendance')
    promoted_to_class = fields.Char(string='Promoted to Class')
    all_dues_paid = fields.Boolean(string='All Dues Paid', default=True)
    
    fee_amount_paid = fields.Monetary(string='Fee Amount Paid', currency_field='currency_id')
    financial_year = fields.Char(string='Financial Year', help="e.g. 2025-2026")
    currency_id = fields.Many2one('res.currency', string='Currency', default=lambda self: self.env.company.currency_id)

    @api.onchange('student_id')
    def _onchange_student_id(self):
        if self.student_id:
            self.class_id = self.student_id.class_id

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', 'New') == 'New':
                vals['name'] = "CertReq"
        res = super().create(vals_list)
        for record in res:
            record.name = f"CERT/{record.id:04d}"
        return res

    def action_approve(self):
        for record in self:
            record.state = 'approved'

    def action_issue(self):
        for record in self:
            record.state = 'issued'
            record.date_issue = fields.Date.context_today(record)

    def action_reject(self):
        for record in self:
            record.state = 'rejected'
