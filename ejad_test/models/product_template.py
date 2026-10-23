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

    def update_quantity_on_hand(self, quantity):
        self.ensure_one()
        product = self.sudo()
        old_quantity = product.qty_available
        warehouse = self.env['stock.warehouse'].sudo().search(
            [('company_id', '=', self.env.company.id)], limit=1)
        quant = self.env['stock.quant'].sudo().with_context(inventory_mode=True).create({
            'product_id': product.product_variant_id.id,
            'location_id': warehouse.lot_stock_id.id,
            'inventory_quantity': quantity,
        })
        quant.action_apply_inventory()
        admins = self.env.ref('stock.group_stock_manager').sudo().users.partner_id - self.env.user.partner_id
        product.message_post(
            partner_ids=admins.ids,
            subject='Product quantity updated: %s' % product.name,
            body='%s updated the quantity of %s from %s to %s.' % (
                self.env.user.name, product.name, old_quantity, product.qty_available),
            subtype_xmlid='mail.mt_comment',
        )

    def action_view_rop_products(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'ROP Products',
            'res_model': 'product.template',
            'view_mode': 'tree,form',
            'domain': [('has_rop', '=', True), ('rop_count', '=', self.rop_count), ('id', '!=', self.id)],
        }
