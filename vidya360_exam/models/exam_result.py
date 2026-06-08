from odoo import models, fields, api

class VidyaExamResult(models.Model):
    _name = 'vidya.exam.result'
    _description = 'Exam Result'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string="Reference", compute="_compute_name", store=True)
    student_id = fields.Many2one('vidya.student', string="Student", required=True)
    schedule_id = fields.Many2one('vidya.exam.schedule', string="Exam Schedule", required=True)
    
    exam_id = fields.Many2one('vidya.exam', related='schedule_id.exam_id', store=True, string="Exam")
    subject_id = fields.Many2one('vidya.subject', related='schedule_id.subject_id', store=True, string="Subject")
    maximum_marks = fields.Float(related='schedule_id.maximum_marks', string="Maximum Marks")
    
    marks_obtained = fields.Float(string="Marks Obtained", required=True)
    grade = fields.Char(string="Grade", compute="_compute_grade", store=True)
    remarks = fields.Text(string="Remarks")

    @api.depends('student_id', 'schedule_id')
    def _compute_name(self):
        for record in self:
            if record.student_id and record.schedule_id:
                record.name = f"Result: {record.student_id.name} - {record.schedule_id.name}"
            else:
                record.name = "New Result"

    @api.depends('marks_obtained', 'maximum_marks')
    def _compute_grade(self):
        for record in self:
            if record.maximum_marks > 0:
                percentage = (record.marks_obtained / record.maximum_marks) * 100
                if percentage >= 90:
                    record.grade = 'A+'
                elif percentage >= 80:
                    record.grade = 'A'
                elif percentage >= 70:
                    record.grade = 'B'
                elif percentage >= 60:
                    record.grade = 'C'
                elif percentage >= 50:
                    record.grade = 'D'
                else:
                    record.grade = 'F'
            else:
                record.grade = ''
