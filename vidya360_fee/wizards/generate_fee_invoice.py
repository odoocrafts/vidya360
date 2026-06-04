from odoo import models, fields, api
from odoo.exceptions import UserError

class GenerateFeeInvoice(models.TransientModel):
    _name = 'vidya.fee.generate.wizard'
    _description = 'Generate Fee Invoice Wizard'

    academic_year_id = fields.Many2one('vidya.academic.year', string='Academic Year', required=True)
    class_id = fields.Many2one('vidya.class.level', string='Class', required=True)
    term_id = fields.Many2one('vidya.academic.term', string='Term', domain="[('year_id', '=', academic_year_id)]")
    month = fields.Selection([
        ('01', 'January'), ('02', 'February'), ('03', 'March'),
        ('04', 'April'), ('05', 'May'), ('06', 'June'),
        ('07', 'July'), ('08', 'August'), ('09', 'September'),
        ('10', 'October'), ('11', 'November'), ('12', 'December')
    ], string='Month')
    frequency = fields.Selection([
        ('monthly', 'Monthly'),
        ('term', 'Term-wise'),
        ('yearly', 'Yearly')
    ], string='Generation Type', required=True, default='term')

    def generate_invoices(self):
        self.ensure_one()
        
        # 1. Find structure
        structure = self.env['vidya.fee.structure'].search([
            ('academic_year_id', '=', self.academic_year_id.id),
            ('class_id', '=', self.class_id.id)
        ], limit=1)
        
        if not structure:
            raise UserError(f"No fee structure found for {self.class_id.name} in {self.academic_year_id.name}")

        lines = structure.line_ids.filtered(lambda l: l.frequency == self.frequency)
        if not lines:
            raise UserError(f"No {self.frequency} fee lines found in structure for {self.class_id.name}")

        # 2. Get students
        students = self.env['vidya.student'].search([
            ('class_id', '=', self.class_id.id),
            ('state', '=', 'enrolled')
        ])

        if not students:
            raise UserError(f"No enrolled students found in {self.class_id.name}")

        # 3. Generate account.move
        moves = []
        for student in students:
            if not student.partner_id:
                raise UserError(f"Student {student.name} does not have an associated contact/partner!")

            invoice_vals = {
                'move_type': 'out_invoice',
                'partner_id': student.partner_id.id,
                'invoice_date': fields.Date.context_today(self),
                'ref': f"Fee: {self.academic_year_id.name} - {self.class_id.name} - {dict(self._fields['frequency'].selection).get(self.frequency)}",
                'invoice_line_ids': []
            }

            for line in lines:
                amount = line.amount
                
                # Check for discounts
                discount = self.env['vidya.student.fee.discount'].search([
                    ('student_id', '=', student.id),
                    ('fee_group_id', '=', line.fee_group_id.id)
                ], limit=1)

                if discount:
                    if discount.discount_type == 'fixed':
                        amount -= discount.discount_value
                    elif discount.discount_type == 'percentage':
                        amount -= amount * (discount.discount_value / 100.0)

                if amount > 0:
                    invoice_vals['invoice_line_ids'].append((0, 0, {
                        'product_id': line.product_id.id,
                        'name': f"{line.fee_group_id.name} ({self.frequency})",
                        'quantity': 1,
                        'price_unit': amount,
                    }))

            if invoice_vals['invoice_line_ids']:
                moves.append(invoice_vals)

        if moves:
            created_moves = self.env['account.move'].create(moves)
            return {
                'name': 'Generated Fee Invoices',
                'type': 'ir.actions.act_window',
                'res_model': 'account.move',
                'view_mode': 'list,form',
                'domain': [('id', 'in', created_moves.ids)],
            }
        else:
            raise UserError("No invoices were generated. This may happen if discounts cover the entire fee amount.")
