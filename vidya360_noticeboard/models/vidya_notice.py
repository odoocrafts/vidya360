from odoo import models, fields, api

class VidyaNotice(models.Model):
    _name = 'vidya.notice'
    _description = 'Notice / Announcement'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'date_posted desc, id desc'

    name = fields.Char(string='Title', required=True, tracking=True)
    content = fields.Html(string='Content', required=True)
    
    date_posted = fields.Datetime(string='Date Posted', default=fields.Datetime.now, required=True, tracking=True)
    date_expiration = fields.Datetime(string='Expiration Date', tracking=True)
    
    audience = fields.Selection([
        ('all', 'All (Staff & Students)'),
        ('staff', 'Staff Only'),
        ('students', 'Students Only')
    ], string='Audience', default='all', required=True, tracking=True)
    
    state = fields.Selection([
        ('draft', 'Draft'),
        ('published', 'Published'),
        ('archived', 'Archived')
    ], string='Status', default='draft', tracking=True)
    
    active = fields.Boolean(default=True)

    def action_publish(self):
        for record in self:
            record.state = 'published'

    def action_archive(self):
        for record in self:
            record.state = 'archived'

    def action_draft(self):
        for record in self:
            record.state = 'draft'
