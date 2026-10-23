from odoo import fields, models


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    has_rop = fields.Boolean(string="Has ROP")
    rop_count = fields.Integer(string="ROP Count")
    rop_product_count = fields.Integer(compute='_compute_rop_product_count')
    above_rop = fields.Boolean(compute='_compute_above_rop', search='_search_above_rop')

    def _compute_rop_product_count(self):
        for product in self:
            product.rop_product_count = product.has_rop and self.search_count([
                ('has_rop', '=', True),
                ('rop_count', '=', product.rop_count),
                ('id', '!=', product._origin.id),
            ])

    def _compute_above_rop(self):
        for product in self:
            product.above_rop = product.has_rop and product.qty_available > product.rop_count

    def _search_above_rop(self, operator, value):
        products = self.search([('has_rop', '=', True)]).filtered(lambda p: p.qty_available > p.rop_count)
        return [('id', 'in', products.ids)]

    def action_view_rop_products(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'ROP Products',
            'res_model': 'product.template',
            'view_mode': 'tree,form',
            'domain': [('has_rop', '=', True), ('rop_count', '=', self.rop_count), ('id', '!=', self.id)],
        }
