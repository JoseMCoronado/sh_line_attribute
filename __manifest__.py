# -*- coding: utf-8 -*-
{
    'name': 'Commissioned Attributes on Sale Order Line',
    'category': 'Sales',
    'author': 'GFP Solutions',
    'summary': 'Custom',
    'version': '1.0',
    'description': """
Adds the ability to add several custom attributes to a sale order line.

THIS MODULE IS PROVIDED AS IS - INSTALLATION AT USERS' OWN RISK - AUTHOR OF MODULE DOES NOT CLAIM ANY
RESPONSIBILITY FOR ANY BEHAVIOR ONCE INSTALLED.
        """,

    'depends':['base','sale'],
    'data':[
            'data/ir_ui_views.xml',
            'data/ir_model_access.xml',
            ],
    'installable': True,
}
