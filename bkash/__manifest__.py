{
    'name': 'bKash Payment Gateway',
    'version': '1.0',
    'category': 'Accounting/Payment Acquirers',
    'summary': 'Integration of bKash Payment Gateway',
    'description': """Pay with bKash directly from Odoo eCommerce and Invoicing.""",
    'author': 'Ayesha Chowdhury',
    'depends': ['base','payment'],
    'data': [
        'data/payment_provider_data.xml',
        'views/payment_bkash_views.xml',
        'security/ir.model.access.csv',
    ],
    'installable': True,
    'application': False,
    'license': 'LGPL-3',
}
