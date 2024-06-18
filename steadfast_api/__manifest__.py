# -*- coding: utf-8 -*-
{
    'name': "Stead Fast",

    'summary': """
        Stead Fast API
        """,

    'description': """
        Stead Fast API
    """,

    'co-author': "Jony Ghosh and Ebna Musab",
    'author': "OXR ITs",
    'website':"http://oxrits.com/",
    'category': 'Sales',
    'version': '15.0.0.1',
    'depends': ['sale'],
    'sequence': -101,
    'data': [
        'security/ir.model.access.csv',
        'views/sale_order_view.xml',
        'views/steadfast_credentials_view.xml',
        'views/steadfast_orders.xml',
        'views/server.xml',
        'views/sale_store_view.xml',
    ],
    'license': "AGPL-3",
    'installable': True,
    'auto-install': False,
    'application': True,
}
