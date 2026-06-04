from odoo import models, fields

class LibraryCategory(models.Model):
    _name = 'vidya.library.category'
    _description = 'Library Category'
    _order = 'name'

    name = fields.Char(string='Category Name', required=True)
    description = fields.Text(string='Description')
    book_ids = fields.One2many('vidya.library.book', 'category_id', string='Books')
    active = fields.Boolean(default=True)
