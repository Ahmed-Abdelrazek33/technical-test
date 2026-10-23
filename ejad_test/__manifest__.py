{
    'name': 'POS Stock Ejad Test',
    'version': '17.0.1.0.0',
    'category': 'Sales/Point of Sale',
    'summary': '',
    'author': 'Ahmed Abdelrazek',
    'license': 'LGPL-3',
    'depends': ['point_of_sale', 'stock'],
    'data': ['views/rop_views.xml'],
    'assets': {
        'point_of_sale._assets_pos': [
            'ejad_test/static/src/js/product_screen.js',
            'ejad_test/static/src/js/cash_now_button.js',
            'ejad_test/static/src/xml/cash_now_button.xml',
        ],
    },
    'installable': True,
    'application': False,
}
