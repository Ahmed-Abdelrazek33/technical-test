import json
from datetime import timedelta

from odoo import fields, http
from odoo.http import request, Response


class PosOrderApi(http.Controller):

    @staticmethod
    def _json_response(payload, status=200):
        return Response(
            json.dumps(payload, ensure_ascii=False, default=str),
            status=status,
            content_type='application/json; charset=utf-8',
        )

    @http.route(
        '/api/pos/orders',
        type='http',
        auth='user',
        methods=['GET'],
        csrf=False,
    )
    def get_pos_orders_by_date(self, start_date=None, end_date=None, **kwargs):
        if not start_date or not end_date:
            return self._json_response({
                'success': False,
                'message': 'start_date and end_date are required. Use YYYY-MM-DD format.',
            }, status=400)

        try:
            start = fields.Date.to_date(start_date)
            end = fields.Date.to_date(end_date)
        except (TypeError, ValueError):
            return self._json_response({
                'success': False,
                'message': 'Invalid date format. Use YYYY-MM-DD.',
            }, status=400)

        if not start or not end:
            return self._json_response({
                'success': False,
                'message': 'Invalid date format. Use YYYY-MM-DD.',
            }, status=400)

        if start > end:
            return self._json_response({
                'success': False,
                'message': 'start_date cannot be greater than end_date.',
            }, status=400)

        start_datetime = fields.Datetime.to_string(fields.Datetime.to_datetime(start))
        end_datetime = fields.Datetime.to_string(
            fields.Datetime.to_datetime(end + timedelta(days=1))
        )

        orders = request.env['pos.order'].sudo().search([
            ('date_order', '>=', start_datetime),
            ('date_order', '<', end_datetime),
        ], order='date_order asc, id asc')

        data = []
        for order in orders:
            data.append({
                'id': order.id,
                'name': order.name,
                'date_order': fields.Datetime.to_string(order.date_order) if order.date_order else False,
                'state': order.state,
                'customer': {
                    'id': order.partner_id.id,
                    'name': order.partner_id.display_name,
                } if order.partner_id else False,
                'session': {
                    'id': order.session_id.id,
                    'name': order.session_id.name,
                } if order.session_id else False,
                'amount_total': order.amount_total,
                'amount_tax': order.amount_tax,
                'currency': order.currency_id.name,
            })

        return self._json_response({
            'success': True,
            'start_date': start_date,
            'end_date': end_date,
            'count': len(data),
            'orders': data,
        })

    @http.route(
        '/api/rop/products',
        type='http',
        auth='user',
        methods=['GET'],
        csrf=False,
    )
    def get_products_with_rop(self, **kwargs):
        """Return all product templates that have ROP enabled and a positive ROP count."""
        products = request.env['product.template'].sudo().search([
            ('has_rop', '=', True),
            ('rop_count', '>', 0),
        ], order='name asc, id asc')

        data = []
        for product in products:
            data.append({
                'id': product.id,
                'name': product.display_name,
                'has_rop': product.has_rop,
                'rop_count': product.rop_count,
                'qty_available': product.qty_available,
            })

        return self._json_response({
            'success': True,
            'count': len(data),
            'products': data,
        })

    @http.route(
        '/api/rop/product',
        type='http',
        auth='user',
        methods=['POST'],
        csrf=False,
    )
    def update_product_rop(self, **kwargs):
        """Set the ROP count for one product template.

        Expected JSON body:
            {
                "product_id": 10,
                "rop_count": 5
            }
        """
        payload = {}
        try:
            if request.httprequest.data:
                payload = json.loads(request.httprequest.data.decode('utf-8'))
        except (ValueError, TypeError, UnicodeDecodeError):
            return self._json_response({
                'success': False,
                'message': 'Invalid JSON body.',
            }, status=400)

        product_id = payload.get('product_id', kwargs.get('product_id'))
        rop_count = payload.get('rop_count', kwargs.get('rop_count'))

        if product_id in (None, '') or rop_count in (None, ''):
            return self._json_response({
                'success': False,
                'message': 'product_id and rop_count are required.',
            }, status=400)

        try:
            product_id = int(product_id)
            rop_count = int(rop_count)
        except (TypeError, ValueError):
            return self._json_response({
                'success': False,
                'message': 'product_id and rop_count must be integers.',
            }, status=400)

        if product_id <= 0:
            return self._json_response({
                'success': False,
                'message': 'product_id must be greater than 0.',
            }, status=400)

        if rop_count < 0:
            return self._json_response({
                'success': False,
                'message': 'rop_count cannot be negative.',
            }, status=400)

        product = request.env['product.template'].sudo().browse(product_id)
        if not product.exists():
            return self._json_response({
                'success': False,
                'message': 'Product not found.',
            }, status=404)

        product.write({
            'has_rop': True,
            'rop_count': rop_count,
        })

        return self._json_response({
            'success': True,
            'message': 'ROP Count updated successfully.',
            'product': {
                'id': product.id,
                'name': product.display_name,
                'has_rop': product.has_rop,
                'rop_count': product.rop_count,
                'qty_available': product.qty_available,
            },
        })

    @http.route(
        '/api/pos/session/<int:session_id>/orders',
        type='http',
        auth='user',
        methods=['GET'],
        csrf=False,
    )
    def get_pos_session_orders(self, session_id, **kwargs):
        """Return all POS orders that belong to the given POS session."""
        session = request.env['pos.session'].sudo().browse(session_id)
        if not session.exists():
            return self._json_response({
                'success': False,
                'message': 'POS Session not found.',
            }, status=404)

        orders = request.env['pos.order'].sudo().search([
            ('session_id', '=', session.id),
        ], order='date_order asc, id asc')

        data = []
        for order in orders:
            data.append({
                'id': order.id,
                'name': order.name,
                'date_order': fields.Datetime.to_string(order.date_order) if order.date_order else False,
                'state': order.state,
                'customer': {
                    'id': order.partner_id.id,
                    'name': order.partner_id.display_name,
                } if order.partner_id else False,
                'amount_total': order.amount_total,
                'amount_tax': order.amount_tax,
                'currency': order.currency_id.name,
            })

        return self._json_response({
            'success': True,
            'session': {
                'id': session.id,
                'name': session.name,
                'state': session.state,
                'config_id': session.config_id.id,
                'config_name': session.config_id.display_name,
            },
            'count': len(data),
            'orders': data,
        })
