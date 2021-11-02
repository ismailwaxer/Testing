# -*- coding: utf-8 -*-
{
    'name': "Sudo Incident Merge",

    'summary': """ This module is design for Merge Incident""",

    'description': """ This module is design for Merge Incident""",
    'author': "SUDO Consultants",
    'website': "http://sudoconsultants.com",
    'price': 10,
    'currency': 'EUR',
    'category': 'Extra Tools',
    'version': '0.2.1',
    'images': ['static/description/img.png'],

    # any module necessary for this one to work correctly
    'depends': ['base', 'sudo_incident', 'helpdesk'],
    'data': [
        'security/ir.model.access.csv',
        'views/sudo_incident_view.xml',
        'wizard/merge_incident_wizard.xml'
        # 'views/templates.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],

}
