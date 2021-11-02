# -*- coding: utf-8 -*-
{
    'name': "SUDO Incident Helpdesk",

    'summary': """
        Short (1 phrase/line) summary of the module's purpose, used as
        subtitle on modules listing or apps.openerp.com""",

    'description': """
        Long description of module's purpose
    """,

    'author': "SUDO Consultants",
    'website': "http://sudoconsultants.com",
    'price': 10,
    'currency': 'EUR',
    'category': 'Extra Tools',
    'version': '0.3',

    # any module necessary for this one to work correctly
    'depends': ['base','sudo_incident','helpdesk'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/views.xml',
        'views/templates.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
