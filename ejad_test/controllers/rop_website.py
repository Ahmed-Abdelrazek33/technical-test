from odoo import http
from odoo.http import request


class ROPWebsiteController(http.Controller):

    @staticmethod
    def _can_access_rop_page():
        user = request.env.user
        return (
            user._is_admin()
            or user.has_group('stock.group_stock_manager')
            or user.has_group('stock.group_stock_user')
        )

    @http.route('/rop', type='http', auth='user', website=True, sitemap=False)
    def rop_page(self, **kwargs):
        """Website ROP page: show products whose ROP Count is below 5."""
        if not self._can_access_rop_page():
            return request.not_found()

        products = request.env['product.template'].sudo().search(
            [('rop_count', '<', 5)],
            order='name asc',
        )

        return request.render('ejad_test.rop_website_page', {
            'products': products,
        })
