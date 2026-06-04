import os

BASE_DIR = '/Users/anas/Documents/Coding/Odoo/odoo19/custom_addons/Vidya360'

# Core Module Files
CORE_FILES = {
    'vidya360_core/__init__.py': "from . import models\n",
    'vidya360_core/__manifest__.py': """{
    'name': 'Vidya 360 Core',
    'version': '19.0.1.0.0',
    'summary': 'Core module for Vidya 360 School ERP',
    'description': 'Provides core academic structure like Academic Year, Terms, Classes, and Subjects.',
    'category': 'Education',
    'author': 'Vidya 360',
    'depends': ['base', 'mail'],
    'data': [
        'security/security_groups.xml',
        'security/ir.model.access.csv',
        'views/menu_views.xml',
        'views/academic_year_views.xml',
        'views/academic_term_views.xml',
        'views/class_level_views.xml',
        'views/section_views.xml',
        'views/subject_views.xml',
    ],
    'installable': True,
    'application': True,
    'license': 'LGPL-3',
}
""",
    'vidya360_core/models/__init__.py': """from . import academic_year
from . import academic_term
from . import class_level
from . import section
from . import subject
""",
    'vidya360_core/models/academic_year.py': """from odoo import models, fields, api

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
""",
    'vidya360_core/models/academic_term.py': """from odoo import models, fields

class AcademicTerm(models.Model):
    _name = 'vidya.academic.term'
    _description = 'Academic Term'
    _order = 'start_date'

    name = fields.Char(string='Term Name', required=True, help="e.g., Term 1, Semester 1")
    year_id = fields.Many2one('vidya.academic.year', string='Academic Year', required=True, ondelete='cascade')
    start_date = fields.Date(string='Start Date', required=True)
    end_date = fields.Date(string='End Date', required=True)
""",
    'vidya360_core/models/class_level.py': """from odoo import models, fields

class ClassLevel(models.Model):
    _name = 'vidya.class.level'
    _description = 'Class / Standard'
    _order = 'sequence, id'

    name = fields.Char(string='Class Name', required=True, help="e.g., Class 1, Grade 10")
    sequence = fields.Integer(string='Sequence', default=10)
    section_ids = fields.One2many('vidya.section', 'class_id', string='Sections')
    active = fields.Boolean(default=True)
""",
    'vidya360_core/models/section.py': """from odoo import models, fields

class Section(models.Model):
    _name = 'vidya.section'
    _description = 'Class Section'
    _order = 'class_id, name'

    name = fields.Char(string='Section Name', required=True, help="e.g., A, B, C")
    class_id = fields.Many2one('vidya.class.level', string='Class', required=True, ondelete='cascade')
    capacity = fields.Integer(string='Capacity', default=30)
    teacher_id = fields.Many2one('res.users', string='Class Teacher', domain="[('share', '=', False)]")
""",
    'vidya360_core/models/subject.py': """from odoo import models, fields

class Subject(models.Model):
    _name = 'vidya.subject'
    _description = 'Subject'
    
    name = fields.Char(string='Subject Name', required=True)
    code = fields.Char(string='Subject Code')
    is_lab = fields.Boolean(string='Is Lab Subject', default=False)
    group_id = fields.Many2one('vidya.subject.group', string='Subject Group')

class SubjectGroup(models.Model):
    _name = 'vidya.subject.group'
    _description = 'Subject Group'

    name = fields.Char(string='Group Name', required=True, help="e.g., Science, Languages")
""",
    'vidya360_core/security/security_groups.xml': """<?xml version="1.0" encoding="utf-8"?>
<odoo>
    <data noupdate="0">
        <record id="module_category_vidya360" model="ir.module.category">
            <field name="name">Vidya 360</field>
            <field name="description">User access level for Vidya 360 ERP.</field>
            <field name="sequence">10</field>
        </record>

        <record id="group_vidya360_student" model="res.groups">
            <field name="name">Student</field>
            <field name="category_id" ref="module_category_vidya360"/>
        </record>

        <record id="group_vidya360_parent" model="res.groups">
            <field name="name">Parent</field>
            <field name="category_id" ref="module_category_vidya360"/>
        </record>

        <record id="group_vidya360_teacher" model="res.groups">
            <field name="name">Teacher</field>
            <field name="category_id" ref="module_category_vidya360"/>
        </record>

        <record id="group_vidya360_principal" model="res.groups">
            <field name="name">Principal</field>
            <field name="category_id" ref="module_category_vidya360"/>
            <field name="implied_ids" eval="[(4, ref('group_vidya360_teacher'))]"/>
        </record>

        <record id="group_vidya360_admin" model="res.groups">
            <field name="name">Administrator</field>
            <field name="category_id" ref="module_category_vidya360"/>
            <field name="implied_ids" eval="[(4, ref('group_vidya360_principal'))]"/>
            <field name="users" eval="[(4, ref('base.user_root')), (4, ref('base.user_admin'))]"/>
        </record>
    </data>
</odoo>
""",
    'vidya360_core/security/ir.model.access.csv': """id,name,model_id:id,group_id:id,perm_read,perm_write,perm_create,perm_unlink
access_vidya_academic_year_admin,vidya.academic.year admin,model_vidya_academic_year,group_vidya360_admin,1,1,1,1
access_vidya_academic_year_user,vidya.academic.year user,model_vidya_academic_year,base.group_user,1,0,0,0
access_vidya_academic_term_admin,vidya.academic.term admin,model_vidya_academic_term,group_vidya360_admin,1,1,1,1
access_vidya_academic_term_user,vidya.academic.term user,model_vidya_academic_term,base.group_user,1,0,0,0
access_vidya_class_level_admin,vidya.class.level admin,model_vidya_class_level,group_vidya360_admin,1,1,1,1
access_vidya_class_level_user,vidya.class.level user,model_vidya_class_level,base.group_user,1,0,0,0
access_vidya_section_admin,vidya.section admin,model_vidya_section,group_vidya360_admin,1,1,1,1
access_vidya_section_user,vidya.section user,model_vidya_section,base.group_user,1,0,0,0
access_vidya_subject_admin,vidya.subject admin,model_vidya_subject,group_vidya360_admin,1,1,1,1
access_vidya_subject_user,vidya.subject user,model_vidya_subject,base.group_user,1,0,0,0
access_vidya_subject_group_admin,vidya.subject.group admin,model_vidya_subject_group,group_vidya360_admin,1,1,1,1
access_vidya_subject_group_user,vidya.subject.group user,model_vidya_subject_group,base.group_user,1,0,0,0
""",
    'vidya360_core/views/menu_views.xml': """<?xml version="1.0" encoding="utf-8"?>
<odoo>
    <!-- Root Menu -->
    <menuitem id="menu_vidya360_root" name="Vidya 360" web_icon="vidya360_core,static/description/icon.png" sequence="10"/>

    <!-- Configuration Menu -->
    <menuitem id="menu_vidya360_configuration" name="Configuration" parent="menu_vidya360_root" sequence="100" groups="group_vidya360_admin"/>
    
    <!-- Academics Config -->
    <menuitem id="menu_vidya360_config_academics" name="Academics" parent="menu_vidya360_configuration" sequence="10"/>
</odoo>
""",
    'vidya360_core/views/academic_year_views.xml': """<?xml version="1.0" encoding="utf-8"?>
<odoo>
    <record id="view_vidya_academic_year_form" model="ir.ui.view">
        <field name="name">vidya.academic.year.form</field>
        <field name="model">vidya.academic.year</field>
        <field name="arch" type="xml">
            <form>
                <sheet>
                    <widget name="web_ribbon" title="Current" bg_color="bg-success" invisible="not is_current"/>
                    <group>
                        <group>
                            <field name="name"/>
                            <field name="start_date"/>
                            <field name="end_date"/>
                        </group>
                        <group>
                            <field name="active" widget="boolean_toggle"/>
                            <field name="is_current"/>
                        </group>
                    </group>
                    <notebook>
                        <page string="Terms">
                            <field name="term_ids">
                                <tree editable="bottom">
                                    <field name="name"/>
                                    <field name="start_date"/>
                                    <field name="end_date"/>
                                </tree>
                            </field>
                        </page>
                    </notebook>
                </sheet>
            </form>
        </field>
    </record>

    <record id="view_vidya_academic_year_tree" model="ir.ui.view">
        <field name="name">vidya.academic.year.tree</field>
        <field name="model">vidya.academic.year</field>
        <field name="arch" type="xml">
            <tree decoration-success="is_current==True">
                <field name="name"/>
                <field name="start_date"/>
                <field name="end_date"/>
                <field name="is_current"/>
                <field name="active" widget="boolean_toggle"/>
            </tree>
        </field>
    </record>

    <record id="action_vidya_academic_year" model="ir.actions.act_window">
        <field name="name">Academic Years</field>
        <field name="res_model">vidya.academic.year</field>
        <field name="view_mode">tree,form</field>
    </record>

    <menuitem id="menu_vidya360_academic_year" name="Academic Years" parent="menu_vidya360_config_academics" action="action_vidya_academic_year" sequence="10"/>
</odoo>
""",
    'vidya360_core/views/academic_term_views.xml': """<?xml version="1.0" encoding="utf-8"?>
<odoo>
    <!-- We use inline tree in academic year form, but defining an action just in case -->
</odoo>
""",
    'vidya360_core/views/class_level_views.xml': """<?xml version="1.0" encoding="utf-8"?>
<odoo>
    <record id="view_vidya_class_level_form" model="ir.ui.view">
        <field name="name">vidya.class.level.form</field>
        <field name="model">vidya.class.level</field>
        <field name="arch" type="xml">
            <form>
                <sheet>
                    <group>
                        <group>
                            <field name="name"/>
                            <field name="sequence"/>
                        </group>
                        <group>
                            <field name="active" widget="boolean_toggle"/>
                        </group>
                    </group>
                    <notebook>
                        <page string="Sections">
                            <field name="section_ids">
                                <tree editable="bottom">
                                    <field name="name"/>
                                    <field name="capacity"/>
                                    <field name="teacher_id"/>
                                </tree>
                            </field>
                        </page>
                    </notebook>
                </sheet>
            </form>
        </field>
    </record>

    <record id="view_vidya_class_level_tree" model="ir.ui.view">
        <field name="name">vidya.class.level.tree</field>
        <field name="model">vidya.class.level</field>
        <field name="arch" type="xml">
            <tree>
                <field name="sequence" widget="handle"/>
                <field name="name"/>
                <field name="active" widget="boolean_toggle"/>
            </tree>
        </field>
    </record>

    <record id="action_vidya_class_level" model="ir.actions.act_window">
        <field name="name">Classes</field>
        <field name="res_model">vidya.class.level</field>
        <field name="view_mode">tree,form</field>
    </record>

    <menuitem id="menu_vidya360_class_level" name="Classes" parent="menu_vidya360_config_academics" action="action_vidya_class_level" sequence="20"/>
</odoo>
""",
    'vidya360_core/views/section_views.xml': """<?xml version="1.0" encoding="utf-8"?>
<odoo>
    <record id="view_vidya_section_form" model="ir.ui.view">
        <field name="name">vidya.section.form</field>
        <field name="model">vidya.section</field>
        <field name="arch" type="xml">
            <form>
                <sheet>
                    <group>
                        <group>
                            <field name="name"/>
                            <field name="class_id"/>
                        </group>
                        <group>
                            <field name="capacity"/>
                            <field name="teacher_id"/>
                        </group>
                    </group>
                </sheet>
            </form>
        </field>
    </record>

    <record id="view_vidya_section_tree" model="ir.ui.view">
        <field name="name">vidya.section.tree</field>
        <field name="model">vidya.section</field>
        <field name="arch" type="xml">
            <tree>
                <field name="class_id"/>
                <field name="name"/>
                <field name="capacity"/>
                <field name="teacher_id"/>
            </tree>
        </field>
    </record>

    <record id="action_vidya_section" model="ir.actions.act_window">
        <field name="name">Sections</field>
        <field name="res_model">vidya.section</field>
        <field name="view_mode">tree,form</field>
    </record>

    <menuitem id="menu_vidya360_section" name="Sections" parent="menu_vidya360_config_academics" action="action_vidya_section" sequence="30"/>
</odoo>
""",
    'vidya360_core/views/subject_views.xml': """<?xml version="1.0" encoding="utf-8"?>
<odoo>
    <record id="view_vidya_subject_form" model="ir.ui.view">
        <field name="name">vidya.subject.form</field>
        <field name="model">vidya.subject</field>
        <field name="arch" type="xml">
            <form>
                <sheet>
                    <group>
                        <group>
                            <field name="name"/>
                            <field name="code"/>
                        </group>
                        <group>
                            <field name="group_id"/>
                            <field name="is_lab"/>
                        </group>
                    </group>
                </sheet>
            </form>
        </field>
    </record>

    <record id="view_vidya_subject_tree" model="ir.ui.view">
        <field name="name">vidya.subject.tree</field>
        <field name="model">vidya.subject</field>
        <field name="arch" type="xml">
            <tree>
                <field name="name"/>
                <field name="code"/>
                <field name="group_id"/>
                <field name="is_lab"/>
            </tree>
        </field>
    </record>

    <record id="action_vidya_subject" model="ir.actions.act_window">
        <field name="name">Subjects</field>
        <field name="res_model">vidya.subject</field>
        <field name="view_mode">tree,form</field>
    </record>

    <menuitem id="menu_vidya360_subject" name="Subjects" parent="menu_vidya360_config_academics" action="action_vidya_subject" sequence="40"/>
</odoo>
"""
}

# Student Module Files
STUDENT_FILES = {
    'vidya360_student/__init__.py': "from . import models\n",
    'vidya360_student/__manifest__.py': """{
    'name': 'Vidya 360 Student Information System',
    'version': '19.0.1.0.0',
    'summary': 'Student management module for Vidya 360',
    'description': 'Manage student profiles, documents, and academic history.',
    'category': 'Education',
    'author': 'Vidya 360',
    'depends': ['vidya360_core'],
    'data': [
        'security/ir.model.access.csv',
        'data/ir_sequence_data.xml',
        'views/student_views.xml',
        'views/menu_views.xml',
    ],
    'installable': True,
    'application': True,
    'license': 'LGPL-3',
}
""",
    'vidya360_student/models/__init__.py': "from . import student\n",
    'vidya360_student/models/student.py': """from odoo import models, fields, api

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
""",
    'vidya360_student/data/ir_sequence_data.xml': """<?xml version="1.0" encoding="utf-8"?>
<odoo>
    <data noupdate="1">
        <record id="seq_vidya_student" model="ir.sequence">
            <field name="name">Student Admission Number</field>
            <field name="code">vidya.student</field>
            <field name="prefix">ADM/%(year)s/</field>
            <field name="padding">4</field>
            <field name="company_id" eval="False"/>
        </record>
    </data>
</odoo>
""",
    'vidya360_student/security/ir.model.access.csv': """id,name,model_id:id,group_id:id,perm_read,perm_write,perm_create,perm_unlink
access_vidya_student_admin,vidya.student admin,model_vidya_student,vidya360_core.group_vidya360_admin,1,1,1,1
access_vidya_student_principal,vidya.student principal,model_vidya_student,vidya360_core.group_vidya360_principal,1,1,1,1
access_vidya_student_teacher,vidya.student teacher,model_vidya_student,vidya360_core.group_vidya360_teacher,1,0,0,0
""",
    'vidya360_student/views/menu_views.xml': """<?xml version="1.0" encoding="utf-8"?>
<odoo>
    <!-- Students Menu -->
    <menuitem id="menu_vidya360_students_root" name="Students" parent="vidya360_core.menu_vidya360_root" sequence="20"/>
    
    <menuitem id="menu_vidya360_students_main" name="Students" parent="menu_vidya360_students_root" action="action_vidya_student" sequence="10"/>
</odoo>
""",
    'vidya360_student/views/student_views.xml': """<?xml version="1.0" encoding="utf-8"?>
<odoo>
    <record id="view_vidya_student_form" model="ir.ui.view">
        <field name="name">vidya.student.form</field>
        <field name="model">vidya.student</field>
        <field name="arch" type="xml">
            <form>
                <sheet>
                    <div class="oe_title">
                        <h1>
                            <field name="name" placeholder="Student Name"/>
                        </h1>
                        <h2>
                            <field name="admission_number"/>
                        </h2>
                    </div>
                    <group>
                        <group string="Academic Information">
                            <field name="academic_year_id"/>
                            <field name="class_id"/>
                            <field name="section_id"/>
                            <field name="roll_number"/>
                        </group>
                        <group string="Personal Information">
                            <field name="gender"/>
                            <field name="date_of_birth"/>
                            <field name="blood_group"/>
                            <field name="aadhaar_number"/>
                            <field name="nationality_id"/>
                            <field name="religion"/>
                        </group>
                    </group>
                    <notebook>
                        <page string="Parent &amp; Guardian">
                            <group>
                                <group>
                                    <field name="father_name"/>
                                    <field name="mother_name"/>
                                    <field name="guardian_name"/>
                                </group>
                                <group>
                                    <field name="phone"/>
                                    <field name="email"/>
                                    <field name="address"/>
                                </group>
                            </group>
                        </page>
                        <page string="Medical">
                            <group>
                                <field name="allergies"/>
                                <field name="health_conditions"/>
                                <field name="emergency_contact"/>
                            </group>
                        </page>
                        <page string="Previous History">
                            <group>
                                <field name="previous_school"/>
                            </group>
                        </page>
                    </notebook>
                </sheet>
                <chatter/>
            </form>
        </field>
    </record>

    <record id="view_vidya_student_tree" model="ir.ui.view">
        <field name="name">vidya.student.tree</field>
        <field name="model">vidya.student</field>
        <field name="arch" type="xml">
            <tree>
                <field name="admission_number"/>
                <field name="name"/>
                <field name="class_id"/>
                <field name="section_id"/>
                <field name="gender"/>
                <field name="phone"/>
            </tree>
        </field>
    </record>

    <record id="view_vidya_student_search" model="ir.ui.view">
        <field name="name">vidya.student.search</field>
        <field name="model">vidya.student</field>
        <field name="arch" type="xml">
            <search>
                <field name="name"/>
                <field name="admission_number"/>
                <field name="class_id"/>
                <separator/>
                <filter string="Archived" name="inactive" domain="[('active', '=', False)]"/>
                <group expand="0" string="Group By">
                    <filter string="Class" name="group_class" context="{'group_by': 'class_id'}"/>
                    <filter string="Section" name="group_section" context="{'group_by': 'section_id'}"/>
                </group>
            </search>
        </field>
    </record>

    <record id="action_vidya_student" model="ir.actions.act_window">
        <field name="name">Students</field>
        <field name="res_model">vidya.student</field>
        <field name="view_mode">tree,form</field>
        <field name="search_view_id" ref="view_vidya_student_search"/>
    </record>
</odoo>
"""
}

def create_files(file_dict):
    for path, content in file_dict.items():
        full_path = os.path.join(BASE_DIR, path)
        os.makedirs(os.path.dirname(full_path), exist_ok=True)
        with open(full_path, 'w') as f:
            f.write(content)

create_files(CORE_FILES)
create_files(STUDENT_FILES)
print("Scaffolding complete!")
