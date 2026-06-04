from odoo import models, fields, api

class CrmLead(models.Model):
    _inherit = 'crm.lead'

    is_student_enquiry = fields.Boolean(string='Is Student Enquiry', default=True)
    student_name = fields.Char(string='Student Name')
    target_class_id = fields.Many2one('vidya.class.level', string='Target Class')
    target_academic_year_id = fields.Many2one('vidya.academic.year', string='Target Academic Year')
    previous_school = fields.Char(string='Previous School')
    father_name = fields.Char(string='Father Name')
    mother_name = fields.Char(string='Mother Name')
    vidya_student_id = fields.Many2one('vidya.student', string='Converted Student', readonly=True)

    def action_convert_to_student(self):
        self.ensure_one()
        if not self.student_name:
            return
        
        student_vals = {
            'name': self.student_name,
            'class_id': self.target_class_id.id,
            'academic_year_id': self.target_academic_year_id.id,
            'previous_school': self.previous_school,
            'father_name': self.father_name,
            'mother_name': self.mother_name,
            'phone': self.phone,
            'email': self.email_from,
        }
        student = self.env['vidya.student'].create(student_vals)
        self.write({
            'vidya_student_id': student.id,
            'probability': 100,
        })
        self.action_set_won()
        
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'vidya.student',
            'res_id': student.id,
            'view_mode': 'form',
            'target': 'current',
        }
