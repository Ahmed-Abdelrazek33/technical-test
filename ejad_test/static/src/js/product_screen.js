/** @odoo-module **/

import { Order } from "@point_of_sale/app/store/models";
import { ErrorPopup } from "@point_of_sale/app/errors/popups/error_popup";
import { patch } from "@web/core/utils/patch";
import { _t } from "@web/core/l10n/translation";
import { PaymentScreen } from "@point_of_sale/app/screens/payment_screen/payment_screen";

patch(Order.prototype, {
    async pay() {
        const productIds = this.get_orderlines().map((line) => line.get_product().id);
        const blocked = await this.env.services.orm.call(
            "pos.session", "check_rop_stock", [[this.pos.pos_session.id], productIds]
        );
        if (blocked.length) {
            return this.env.services.popup.add(ErrorPopup, {
                title: _t("Re-Order Point Validation"),
                body: _t("This product under of the Re-Order Point measure") + "\n" + blocked.join("\n"),
            });
        }
        return super.pay(...arguments);
    },
});

