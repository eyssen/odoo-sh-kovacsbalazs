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
    'depends' : ['base', 'project', 'website_blog'],
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'views/project.xml',
        'views/loader.xml',
        'views/account_analytic_line.xml',
        'views/employee.xml',
        'views/digest.xml',
    ],
    'qweb': [],
    'installable': True,
    'application': True,
    'auto_install': False,
}
