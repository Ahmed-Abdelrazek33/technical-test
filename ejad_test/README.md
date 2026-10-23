# POS Stock Reorder Point Validation — Odoo 17

## Installation
1. Extract this archive into your custom addons directory.
2. Restart Odoo, update the Apps list, and install POS Stock Reorder Point Validation.
3. Close/reopen or fully reload the POS browser so the new assets load.
4. Confirm the POS operation type is linked to the intended warehouse.

## Behavior
Clicking Payment on the products screen checks every distinct product in the
current order using a fresh server request. Stockable products must have more
than 5 available units (on hand minus reserved) in the POS operation type's
warehouse, using the product's inventory unit of measure. Exactly 5 is blocked.
Services and consumables are skipped because they do not track stock in Odoo 17.
The popup shows the requested message plus all blocked products and quantities.
The threshold is fixed at 5; configured Odoo replenishment rules are not consulted.
The check compares current availability, not availability minus order quantity.
All products in the order are checked, including stockable refund lines.

The check requires an online connection and fails closed when unavailable.
It does not reserve stock: other sessions can change stock after the check.
Scope is the standard product-screen Payment action, not backend imports or
custom flows that navigate directly to payment. No notifications are created.

## Manual acceptance checks on a test database
- Stockable product free quantity 6: Payment opens normally.
- Free quantity 5, 4, 0, or negative: popup; remain on product screen.
- Mixed order: a single blocked product prevents payment; list all failures.
- Stock in a different warehouse must not allow the order to pass.
- On hand 10, reserved 6: free quantity 4 blocks payment.
- Services/consumables alone: normal payment flow.
- Disconnect network: payment stays blocked with Stock Check Failed.
- Change stock externally then retry Payment: fresh quantity is used.
- Existing standard POS payment restrictions still apply after a successful check.

## Validation status
Python/JavaScript syntax and ZIP structure checked during packaging.
An Odoo 17 instance was not available for installation or browser integration testing.

## API Task 1 - POS Orders by Date Range

Endpoint:

```text
GET /api/pos/orders?start_date=YYYY-MM-DD&end_date=YYYY-MM-DD
```

Authentication: logged-in Odoo user (`auth='user'`).

Example:

```text
/api/pos/orders?start_date=2026-10-01&end_date=2026-10-23
```

The date range is inclusive. The response contains the POS order ID, reference,
order date, state, customer, POS session, total, tax, and currency.
