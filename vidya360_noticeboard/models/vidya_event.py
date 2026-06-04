from odoo import models, fields, api

class VidyaEvent(models.Model):
    _name = 'vidya.event'
    _description = 'School Event'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'start_date'

    name = fields.Char(string='Event Name', required=True, tracking=True)
    event_type = fields.Selection([
        ('academic', 'Academic'),
        ('holiday', 'Holiday'),
        ('sports', 'Sports'),
        ('meeting', 'Meeting'),
        ('other', 'Other')
    ], string='Event Type', default='other', required=True, tracking=True)
    
    start_date = fields.Datetime(string='Start Date', required=True, tracking=True)
    end_date = fields.Datetime(string='End Date', required=True, tracking=True)
    
    all_day = fields.Boolean(string='All Day', default=True)
    location = fields.Char(string='Location')
    description = fields.Html(string='Description')
    
    active = fields.Boolean(default=True)
