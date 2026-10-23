/** @odoo-module **/

import { Order } from "@point_of_sale/app/store/models";
import { ErrorPopup } from "@point_of_sale/app/errors/popups/error_popup";
import { onMounted } from "@odoo/owl";
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
            this.cashNow = false;
            return this.env.services.popup.add(ErrorPopup, {
                title: _t("Re-Order Point Validation"),
                body: _t("This product under of the Re-Order Point measure") + "\n" + blocked.join("\n"),
            });
        }
        return super.pay(...arguments);
    },
});

patch(PaymentScreen.prototype, {
    setup() {
        super.setup(...arguments);
        onMounted(() => {
            if (this.currentOrder.cashNow) {
                this.currentOrder.cashNow = false;
                this.currentOrder.add_paymentline(this.pos.payment_methods.find((m) => m.is_cash_count));
                this.validateOrder();
            }
        });
    },
    async validateOrder() {
        const partner = this.currentOrder.get_partner();
        const phone = partner && partner.phone;
        const error = !partner ? _t("Please select a customer.")
            : !phone ? _t("The customer must have a phone number.")
            : !phone.startsWith("+2") ? _t("The customer phone must start with +2.")
            : "";
        if (error) {
            return this.popup.add(ErrorPopup, { title: _t("Customer Validation"), body: error });
        }
        return super.validateOrder(...arguments);
    },
});
