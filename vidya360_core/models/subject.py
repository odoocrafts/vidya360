from odoo import models, fields

class Subject(models.Model):
    _name = 'vidya.subject'
    _description = 'Subject'
    
    name = fields.Char(string='Subject Name', required=True)
    code = fields.Char(string='Subject Code')
    is_lab = fields.Boolean(string='Is Lab Subject', default=False)
    is_elective = fields.Boolean(string='Is Elective Subject', default=False)
    group_id = fields.Many2one('vidya.subject.group', string='Subject Group')

class SubjectGroup(models.Model):
    _name = 'vidya.subject.group'
    _description = 'Subject Group'

    name = fields.Char(string='Group Name', required=True, help="e.g., Science, Languages")
