import os

BASE_DIR = '/Users/anas/Documents/Coding/Odoo/odoo19/custom_addons/Vidya360'

ADMISSION_FILES = {
    'vidya360_admission/__init__.py': "from . import models\n",
    'vidya360_admission/__manifest__.py': """{
    'name': 'Vidya 360 Admissions CRM',
    'version': '19.0.1.0.0',
    'summary': 'Manage student enquiries and admissions',
    'category': 'Education',
    'author': 'Vidya 360',
    'depends': ['crm', 'vidya360_student'],
    'data': [
        'data/crm_stage_data.xml',
        'views/crm_lead_views.xml',
        'views/menu_views.xml',
    ],
    'installable': True,
    'application': True,
    'license': 'LGPL-3',
}
""",
    'vidya360_admission/models/__init__.py': "from . import crm_lead\n",
    'vidya360_admission/models/crm_lead.py': """from odoo import models, fields, api

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
""",
    'vidya360_admission/data/crm_stage_data.xml': """<?xml version="1.0" encoding="utf-8"?>
<odoo>
    <data noupdate="1">
        <record id="crm_stage_enquiry" model="crm.stage">
            <field name="name">New Enquiry</field>
            <field name="sequence">1</field>
        </record>
        <record id="crm_stage_visit" model="crm.stage">
            <field name="name">Campus Visit</field>
            <field name="sequence">2</field>
        </record>
        <record id="crm_stage_applied" model="crm.stage">
            <field name="name">Application Submitted</field>
            <field name="sequence">3</field>
        </record>
        <record id="crm_stage_interview" model="crm.stage">
            <field name="name">Interview Scheduled</field>
            <field name="sequence">4</field>
        </record>
        <record id="crm_stage_admitted" model="crm.stage">
            <field name="name">Admission Confirmed</field>
            <field name="sequence">5</field>
            <field name="is_won">True</field>
        </record>
    </data>
</odoo>
""",
    'vidya360_admission/views/crm_lead_views.xml': """<?xml version="1.0" encoding="utf-8"?>
<odoo>
    <record id="view_crm_lead_form_inherit_vidya" model="ir.ui.view">
        <field name="name">crm.lead.form.inherit.vidya</field>
        <field name="model">crm.lead</field>
        <field name="inherit_id" ref="crm.crm_lead_view_form"/>
        <field name="arch" type="xml">
            <xpath expr="//header" position="inside">
                <button name="action_convert_to_student" string="Convert to Student" type="object" class="oe_highlight" invisible="vidya_student_id or type == 'opportunity' and probability == 100"/>
            </xpath>
            <xpath expr="//notebook/page[@name='internal_notes']" position="before">
                <page string="Admission Details" name="admission_details">
                    <group>
                        <group>
                            <field name="is_student_enquiry"/>
                            <field name="student_name" required="is_student_enquiry"/>
                            <field name="target_class_id"/>
                            <field name="target_academic_year_id"/>
                        </group>
                        <group>
                            <field name="father_name"/>
                            <field name="mother_name"/>
                            <field name="previous_school"/>
                            <field name="vidya_student_id"/>
                        </group>
                    </group>
                </page>
            </xpath>
        </field>
    </record>

    <record id="action_vidya_admission" model="ir.actions.act_window">
        <field name="name">Admissions Pipeline</field>
        <field name="res_model">crm.lead</field>
        <field name="view_mode">kanban,list,graph,pivot,calendar,form,activity</field>
        <field name="domain">[('is_student_enquiry', '=', True)]</field>
        <field name="context">{'default_is_student_enquiry': True}</field>
    </record>
</odoo>
""",
    'vidya360_admission/views/menu_views.xml': """<?xml version="1.0" encoding="utf-8"?>
<odoo>
    <menuitem id="menu_vidya360_admissions" name="Admissions" parent="vidya360_core.menu_vidya360_root" sequence="10"/>
    
    <menuitem id="menu_vidya360_admissions_pipeline" name="Pipeline" parent="menu_vidya360_admissions" action="action_vidya_admission" sequence="10"/>
</odoo>
"""
}

ATTENDANCE_FILES = {
    'vidya360_attendance/__init__.py': "from . import models\n",
    'vidya360_attendance/__manifest__.py': """{
    'name': 'Vidya 360 Attendance',
    'version': '19.0.1.0.0',
    'summary': 'Manage daily student attendance',
    'category': 'Education',
    'author': 'Vidya 360',
    'depends': ['vidya360_student'],
    'data': [
        'security/ir.model.access.csv',
        'views/attendance_views.xml',
        'views/attendance_sheet_views.xml',
        'views/menu_views.xml',
    ],
    'installable': True,
    'application': True,
    'license': 'LGPL-3',
}
""",
    'vidya360_attendance/models/__init__.py': """from . import attendance
from . import attendance_sheet
""",
    'vidya360_attendance/models/attendance.py': """from odoo import models, fields

class StudentAttendance(models.Model):
    _name = 'vidya.attendance'
    _description = 'Student Attendance Record'

    student_id = fields.Many2one('vidya.student', string='Student', required=True)
    date = fields.Date(string='Date', required=True, default=fields.Date.context_today)
    status = fields.Selection([
        ('present', 'Present'),
        ('absent', 'Absent'),
        ('half_day', 'Half Day'),
        ('leave', 'Leave')
    ], string='Status', required=True, default='present')
    remarks = fields.Char(string='Remarks')
    sheet_id = fields.Many2one('vidya.attendance.sheet', string='Attendance Sheet', ondelete='cascade')

    _sql_constraints = [
        ('unique_student_date', 'unique(student_id, date)', 'A student can only have one attendance record per day!')
    ]
""",
    'vidya360_attendance/models/attendance_sheet.py': """from odoo import models, fields, api

class AttendanceSheet(models.Model):
    _name = 'vidya.attendance.sheet'
    _description = 'Class Attendance Sheet'

    name = fields.Char(string='Reference', compute='_compute_name')
    class_id = fields.Many2one('vidya.class.level', string='Class', required=True)
    section_id = fields.Many2one('vidya.section', string='Section', required=True, domain="[('class_id', '=', class_id)]")
    date = fields.Date(string='Date', required=True, default=fields.Date.context_today)
    state = fields.Selection([
        ('draft', 'Draft'),
        ('done', 'Submitted')
    ], string='State', default='draft')
    attendance_ids = fields.One2many('vidya.attendance', 'sheet_id', string='Attendances')

    @api.depends('section_id', 'date')
    def _compute_name(self):
        for sheet in self:
            if sheet.section_id and sheet.date:
                sheet.name = f"{sheet.section_id.class_id.name} {sheet.section_id.name} - {sheet.date}"
            else:
                sheet.name = "New Sheet"

    def action_load_students(self):
        self.ensure_one()
        students = self.env['vidya.student'].search([
            ('section_id', '=', self.section_id.id),
            ('active', '=', True)
        ])
        
        # Keep existing records for today
        existing_student_ids = self.attendance_ids.mapped('student_id').ids
        
        vals_list = []
        for student in students:
            if student.id not in existing_student_ids:
                vals_list.append((0, 0, {
                    'student_id': student.id,
                    'date': self.date,
                    'status': 'present'
                }))
        
        if vals_list:
            self.write({'attendance_ids': vals_list})

    def action_submit(self):
        self.write({'state': 'done'})
""",
    'vidya360_attendance/security/ir.model.access.csv': """id,name,model_id:id,group_id:id,perm_read,perm_write,perm_create,perm_unlink
access_vidya_attendance_admin,vidya.attendance admin,model_vidya_attendance,vidya360_core.group_vidya360_admin,1,1,1,1
access_vidya_attendance_teacher,vidya.attendance teacher,model_vidya_attendance,vidya360_core.group_vidya360_teacher,1,1,1,0
access_vidya_attendance_sheet_admin,vidya.attendance.sheet admin,model_vidya_attendance_sheet,vidya360_core.group_vidya360_admin,1,1,1,1
access_vidya_attendance_sheet_teacher,vidya.attendance.sheet teacher,model_vidya_attendance_sheet,vidya360_core.group_vidya360_teacher,1,1,1,0
""",
    'vidya360_attendance/views/attendance_views.xml': """<?xml version="1.0" encoding="utf-8"?>
<odoo>
    <record id="view_vidya_attendance_list" model="ir.ui.view">
        <field name="name">vidya.attendance.list</field>
        <field name="model">vidya.attendance</field>
        <field name="arch" type="xml">
            <list editable="bottom" decoration-danger="status=='absent'" decoration-warning="status=='half_day'" decoration-info="status=='leave'">
                <field name="date"/>
                <field name="student_id"/>
                <field name="status"/>
                <field name="remarks"/>
            </list>
        </field>
    </record>

    <record id="view_vidya_attendance_search" model="ir.ui.view">
        <field name="name">vidya.attendance.search</field>
        <field name="model">vidya.attendance</field>
        <field name="arch" type="xml">
            <search>
                <field name="student_id"/>
                <field name="date"/>
                <filter string="Today" name="today" domain="[('date', '=', context_today().strftime('%Y-%m-%d'))]"/>
                <filter string="Absents" name="absents" domain="[('status', '=', 'absent')]"/>
                <group expand="0" string="Group By">
                    <filter string="Student" name="group_student" context="{'group_by': 'student_id'}"/>
                    <filter string="Date" name="group_date" context="{'group_by': 'date'}"/>
                    <filter string="Status" name="group_status" context="{'group_by': 'status'}"/>
                </group>
            </search>
        </field>
    </record>

    <record id="action_vidya_attendance" model="ir.actions.act_window">
        <field name="name">Student Attendance</field>
        <field name="res_model">vidya.attendance</field>
        <field name="view_mode">list</field>
        <field name="search_view_id" ref="view_vidya_attendance_search"/>
    </record>
</odoo>
""",
    'vidya360_attendance/views/attendance_sheet_views.xml': """<?xml version="1.0" encoding="utf-8"?>
<odoo>
    <record id="view_vidya_attendance_sheet_form" model="ir.ui.view">
        <field name="name">vidya.attendance.sheet.form</field>
        <field name="model">vidya.attendance.sheet</field>
        <field name="arch" type="xml">
            <form>
                <header>
                    <button name="action_load_students" string="Load Students" type="object" class="oe_highlight" invisible="state != 'draft'"/>
                    <button name="action_submit" string="Submit" type="object" class="oe_highlight" invisible="state != 'draft'"/>
                    <field name="state" widget="statusbar"/>
                </header>
                <sheet>
                    <div class="oe_title">
                        <h1><field name="name" readonly="1"/></h1>
                    </div>
                    <group>
                        <group>
                            <field name="class_id" readonly="state != 'draft'"/>
                            <field name="section_id" readonly="state != 'draft'"/>
                        </group>
                        <group>
                            <field name="date" readonly="state != 'draft'"/>
                        </group>
                    </group>
                    <notebook>
                        <page string="Attendances">
                            <field name="attendance_ids" readonly="state != 'draft'">
                                <list editable="bottom" decoration-danger="status=='absent'" decoration-warning="status=='half_day'" decoration-info="status=='leave'">
                                    <field name="student_id" readonly="1"/>
                                    <field name="date" column_invisible="1"/>
                                    <field name="status"/>
                                    <field name="remarks"/>
                                </list>
                            </field>
                        </page>
                    </notebook>
                </sheet>
            </form>
        </field>
    </record>

    <record id="view_vidya_attendance_sheet_list" model="ir.ui.view">
        <field name="name">vidya.attendance.sheet.list</field>
        <field name="model">vidya.attendance.sheet</field>
        <field name="arch" type="xml">
            <list decoration-muted="state=='done'">
                <field name="name"/>
                <field name="class_id"/>
                <field name="section_id"/>
                <field name="date"/>
                <field name="state" widget="badge" decoration-success="state=='done'" decoration-info="state=='draft'"/>
            </list>
        </field>
    </record>

    <record id="action_vidya_attendance_sheet" model="ir.actions.act_window">
        <field name="name">Attendance Sheets</field>
        <field name="res_model">vidya.attendance.sheet</field>
        <field name="view_mode">list,form</field>
    </record>
</odoo>
""",
    'vidya360_attendance/views/menu_views.xml': """<?xml version="1.0" encoding="utf-8"?>
<odoo>
    <menuitem id="menu_vidya360_attendance_root" name="Attendance" parent="vidya360_core.menu_vidya360_root" sequence="30"/>
    
    <menuitem id="menu_vidya360_attendance_sheets" name="Attendance Sheets" parent="menu_vidya360_attendance_root" action="action_vidya_attendance_sheet" sequence="10"/>
    <menuitem id="menu_vidya360_attendance_records" name="Attendance Records" parent="menu_vidya360_attendance_root" action="action_vidya_attendance" sequence="20"/>
</odoo>
"""
}

def create_files(file_dict):
    for path, content in file_dict.items():
        full_path = os.path.join(BASE_DIR, path)
        os.makedirs(os.path.dirname(full_path), exist_ok=True)
        with open(full_path, 'w') as f:
            f.write(content)

create_files(ADMISSION_FILES)
create_files(ATTENDANCE_FILES)
print("Phase 2 Scaffolding complete!")
