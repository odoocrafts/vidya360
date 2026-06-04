from odoo import models, fields

class StudentFeeDiscount(models.Model):
    _name = 'vidya.student.fee.discount'
    _description = 'Student Fee Discount / Override'

    student_id = fields.Many2one('vidya.student', string='Student', required=True, ondelete='cascade')
    fee_group_id = fields.Many2one('vidya.fee.group', string='Fee Group', required=True)
    discount_type = fields.Selection([
        ('percentage', 'Percentage (%)'),
        ('fixed', 'Fixed Amount')
    ], string='Discount Type', required=True, default='percentage')
    discount_value = fields.Float(string='Discount Value', required=True)
    reason = fields.Char(string='Reason', help="e.g., Scholarship, Staff Child")
    active = fields.Boolean(default=True)

class VidyaStudent(models.Model):
    _inherit = 'vidya.student'

    discount_ids = fields.One2many('vidya.student.fee.discount', 'student_id', string='Fee Discounts')
