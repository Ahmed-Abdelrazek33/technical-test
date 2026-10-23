/** @odoo-module **/

import { Component } from "@odoo/owl";
import { ProductScreen } from "@point_of_sale/app/screens/product_screen/product_screen";
import { usePos } from "@point_of_sale/app/store/pos_hook";

export class CashNowButton extends Component {
    static template = "ejad_test.CashNowButton";

    setup() {
        this.pos = usePos();
    }

    async onClick() {
        const order = this.pos.get_order();
        order.set_partner(this.pos.db.search_partner("admin")[0]);
        order.set_to_invoice(true);
        order.cashNow = true;
        await order.pay();
    }
}

ProductScreen.addControlButton({ component: CashNowButton, condition: () => true });
