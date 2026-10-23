from odoo import fields, models
from odoo.exceptions import ValidationError


class StockPicking(models.Model):
    _inherit = 'stock.picking'

    def button_validate(self):
        today = fields.Date.context_today(self)
        for picking in self:
            if (picking.picking_type_code == 'outgoing'
                    and fields.Date.context_today(self, picking.scheduled_date) >= today):
                raise ValidationError("You cannot validate an outgoing picking scheduled today or later.")
        return super().button_validate()
