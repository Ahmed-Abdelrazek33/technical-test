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
