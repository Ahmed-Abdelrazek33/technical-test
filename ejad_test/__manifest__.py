{
    'name': 'POS Stock Ejad Test',
    'version': '17.0.1.0.0',
    'category': 'Sales/Point of Sale',
    'summary': '',
    'author': 'Ahmed Abdelrazek',
    'license': 'LGPL-3',
    'depends': ['point_of_sale', 'stock'],
    'assets': {
        'point_of_sale._assets_pos': [
            'ejad_test/static/src/js/product_screen.js',
        ],
    },
    'installable': True,
    'application': False,
}
