from odoo import models


class WebsiteMenu(models.Model):
    _inherit = "website.menu"

    def _compute_visible(self):
        super()._compute_visible()

        user = self.env.user
        can_see_rop = (
            user._is_admin()
            or user.has_group("stock.group_stock_manager")
            or user.has_group("stock.group_stock_user")
        )

        for menu in self:
            if menu.url in ("/rop", "/rop/realtime", "/rop/api") and not can_see_rop:
                menu.is_visible = False
