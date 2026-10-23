from odoo import models


class PosSession(models.Model):
    _inherit = 'pos.session'

    def check_rop_stock(self, product_ids):
        """Return names of stockable products with free qty <= 5 and notify warehouse admins."""
        warehouse = self.config_id.picking_type_id.warehouse_id
        products = self.env['product.product'].sudo().browse(product_ids).with_context(
            warehouse=warehouse.id)
        names = [p.display_name for p in products if p.type == 'product' and p.free_qty <= 5]
        if names:
            admins = self.env.ref('stock.group_stock_manager').sudo().users.partner_id
            self.sudo().message_post(
                partner_ids=admins.ids,
                subject='Re-Order Point alert: %s' % warehouse.name,
                body='Please check the Re-Order Point of: %s' % ', '.join(names),
                subtype_xmlid='mail.mt_comment',
            )
        return names
