from odoo import models, fields, api

class FeeStructure(models.Model):
    _name = 'vidya.fee.structure'
    _description = 'Fee Structure'

    name = fields.Char(string='Reference', required=True, default='New')
    academic_year_id = fields.Many2one('vidya.academic.year', string='Academic Year', required=True)
    class_id = fields.Many2one('vidya.class.level', string='Class', required=True)
    active = fields.Boolean(default=True)
    
    line_ids = fields.One2many('vidya.fee.structure.line', 'structure_id', string='Fee Details')

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', 'New') == 'New':
                vals['name'] = "Fee Structure"
        res = super().create(vals_list)
        for record in res:
            record.name = f"{record.class_id.name} - {record.academic_year_id.name}"
        return res

class FeeStructureLine(models.Model):
    _name = 'vidya.fee.structure.line'
    _description = 'Fee Structure Line'

    structure_id = fields.Many2one('vidya.fee.structure', string='Structure', required=True, ondelete='cascade')
    fee_group_id = fields.Many2one('vidya.fee.group', string='Fee Group', required=True)
    amount = fields.Float(string='Amount', required=True)
    frequency = fields.Selection([
        ('monthly', 'Monthly'),
        ('term', 'Term-wise'),
        ('yearly', 'Yearly')
    ], string='Frequency', required=True, default='term')
    product_id = fields.Many2one('product.product', string='Accounting Product', required=True, 
                                 help="Used to map this fee to the correct income account in standard accounting.")
