from odoo import models, fields, api

class VidyaExamSchedule(models.Model):
    _name = 'vidya.exam.schedule'
    _description = 'Exam Schedule'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string="Reference", compute="_compute_name", store=True)
    exam_id = fields.Many2one('vidya.exam', string="Exam", required=True, ondelete='cascade')
    subject_id = fields.Many2one('vidya.subject', string="Subject", required=True)
    
    class_level_id = fields.Many2one('vidya.class.level', string="Class Level", required=True)
    section_id = fields.Many2one('vidya.section', string="Section") # Optional, if it's for the whole class
    
    date = fields.Date(string="Exam Date", required=True)
    start_time = fields.Float(string="Start Time", required=True)
    end_time = fields.Float(string="End Time", required=True)
    
    maximum_marks = fields.Float(string="Maximum Marks", required=True, default=100.0)

    @api.depends('exam_id', 'subject_id', 'class_level_id')
    def _compute_name(self):
        for record in self:
            if record.exam_id and record.subject_id and record.class_level_id:
                record.name = f"{record.exam_id.name} - {record.subject_id.name} ({record.class_level_id.name})"
            else:
                record.name = "New Schedule"
