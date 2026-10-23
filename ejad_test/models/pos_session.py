from odoo import models


class PosSession(models.Model):
    _inherit = 'pos.session'

    def check_rop_stock(self, product_ids):
        """Return names of stockable products with free qty <= 5 in the POS warehouse."""
        warehouse = self.config_id.picking_type_id.warehouse_id
        products = self.env['product.product'].sudo().browse(product_ids).with_context(
            warehouse=warehouse.id)
        return [p.display_name for p in products if p.type == 'product' and p.free_qty <= 5]
