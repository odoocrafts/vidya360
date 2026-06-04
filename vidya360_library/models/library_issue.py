from odoo import models, fields, api
from odoo.exceptions import UserError
from datetime import timedelta

class LibraryIssue(models.Model):
    _name = 'vidya.library.issue'
    _description = 'Book Issue / Return'
    _order = 'date_issue desc, id desc'

    name = fields.Char(string='Reference', required=True, copy=False, readonly=True, default='New')
    book_id = fields.Many2one('vidya.library.book', string='Book', required=True)
    
    member_type = fields.Selection([
        ('student', 'Student'),
        ('staff', 'Staff')
    ], string='Borrower Type', default='student', required=True)
    
    student_id = fields.Many2one('vidya.student', string='Student')
    staff_id = fields.Many2one('hr.employee', string='Staff')
    
    date_issue = fields.Date(string='Issue Date', default=fields.Date.context_today, required=True)
    date_due = fields.Date(string='Due Date', default=lambda self: fields.Date.context_today(self) + timedelta(days=14), required=True)
    date_return = fields.Date(string='Return Date')
    
    state = fields.Selection([
        ('draft', 'Draft'),
        ('issued', 'Issued'),
        ('returned', 'Returned'),
        ('overdue', 'Overdue')
    ], string='Status', default='draft', required=True, tracking=True)
    
    fine_amount = fields.Monetary(string='Late Fine', currency_field='currency_id')
    currency_id = fields.Many2one('res.currency', string='Currency', default=lambda self: self.env.company.currency_id)
    
    company_id = fields.Many2one('res.company', string='Company', default=lambda self: self.env.company)

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', 'New') == 'New':
                vals['name'] = self.env['ir.sequence'].next_by_code('vidya.library.issue') or 'New'
        return super().create(vals_list)

    def action_issue(self):
        for record in self:
            if record.book_id.available_copies <= 0:
                raise UserError("There are no available copies of this book!")
            if record.member_type == 'student' and not record.student_id:
                raise UserError("Please select a student.")
            if record.member_type == 'staff' and not record.staff_id:
                raise UserError("Please select a staff member.")
            record.state = 'issued'
            
    def action_return(self):
        for record in self:
            record.state = 'returned'
            record.date_return = fields.Date.context_today(self)
            
            # Simple fine calculation if overdue
            if record.date_return > record.date_due:
                days_late = (record.date_return - record.date_due).days
                # Default fine: 5 per day late
                record.fine_amount = days_late * 5.0
