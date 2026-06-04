from odoo import models, fields, api

class LibraryBook(models.Model):
    _name = 'vidya.library.book'
    _description = 'Library Book'
    _order = 'name'

    name = fields.Char(string='Title', required=True)
    author = fields.Char(string='Author(s)')
    isbn = fields.Char(string='ISBN')
    barcode = fields.Char(string='Barcode')
    publisher = fields.Char(string='Publisher')
    category_id = fields.Many2one('vidya.library.category', string='Category')
    edition = fields.Char(string='Edition')
    location = fields.Char(string='Shelf/Location')
    
    total_copies = fields.Integer(string='Total Copies', default=1, required=True)
    available_copies = fields.Integer(string='Available Copies', compute='_compute_available_copies', store=True)
    
    issue_ids = fields.One2many('vidya.library.issue', 'book_id', string='Issues')
    active = fields.Boolean(default=True)
    
    image_1920 = fields.Image("Image", max_width=1920, max_height=1920)

    @api.depends('total_copies', 'issue_ids.state')
    def _compute_available_copies(self):
        for book in self:
            issued_count = len(book.issue_ids.filtered(lambda i: i.state == 'issued'))
            book.available_copies = book.total_copies - issued_count
