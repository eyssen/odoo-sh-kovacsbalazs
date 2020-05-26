# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name' : 'KBL',
    'version' : '1.0',
    'summary': 'KBL Addon',
    'sequence': 15,
    'description': """
KBL Addon
    """,
    'category': 'Other',
    'website': 'https://www.eyssen.hu',
    'depends' : [],
    'data': [
        'views/project.xml',
        'views/loader.xml',
    ],
    'qweb': [],
    'installable': True,
    'application': True,
    'auto_install': False,
}
