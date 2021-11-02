# -*- coding: utf-8 -*-
{
    'name': "SUDO Helpdesk date",

    'summary': """This module is design for adding Date to Helpdesk""",

    'description': """This module is design for adding Date to Helpdesk""",

    'author': "SUDO Consultants",
    'website': "https://sudoconsultants.com/",
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'helpdesk'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/views.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
