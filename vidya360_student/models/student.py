from odoo import models, fields, api

class Student(models.Model):
    _name = 'vidya.student'
    _description = 'Student Profile'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    # Personal Information
    name = fields.Char(string='Student Name', required=True, tracking=True)
    admission_number = fields.Char(string='Admission Number', required=True, copy=False, readonly=True, default=lambda self: 'New')
    roll_number = fields.Char(string='Roll Number')
    gender = fields.Selection([('male', 'Male'), ('female', 'Female'), ('other', 'Other')], string='Gender')
    date_of_birth = fields.Date(string='Date of Birth')
    blood_group = fields.Selection([
        ('a+', 'A+'), ('a-', 'A-'), ('b+', 'B+'), ('b-', 'B-'),
        ('ab+', 'AB+'), ('ab-', 'AB-'), ('o+', 'O+'), ('o-', 'O-')
    ], string='Blood Group')
    aadhaar_number = fields.Char(string='Aadhaar Number')
    religion = fields.Char(string='Religion')
    nationality_id = fields.Many2one('res.country', string='Nationality')

    # Academic Information
    class_id = fields.Many2one('vidya.class.level', string='Class', tracking=True)
    section_id = fields.Many2one('vidya.section', string='Section', domain="[('class_id', '=', class_id)]", tracking=True)
    academic_year_id = fields.Many2one('vidya.academic.year', string='Academic Year', tracking=True)
    previous_school = fields.Char(string='Previous School')
    elective_subject_ids = fields.Many2many('vidya.subject', string='Elective Subjects', domain="[('is_elective', '=', True)]")

    # Parent Information
    father_name = fields.Char(string='Father Name')
    mother_name = fields.Char(string='Mother Name')
    guardian_name = fields.Char(string='Guardian Name')
    phone = fields.Char(string='Phone')
    email = fields.Char(string='Email')
    address = fields.Text(string='Address')

    # Medical
    allergies = fields.Text(string='Allergies')
    health_conditions = fields.Text(string='Health Conditions')
    emergency_contact = fields.Char(string='Emergency Contact Number')
    
    active = fields.Boolean(default=True)

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('admission_number', 'New') == 'New':
                vals['admission_number'] = self.env['ir.sequence'].next_by_code('vidya.student') or 'New'
        return super().create(vals_list)
