# -*- coding: utf-8 -*-
{
    'name': "SUDO CMDB",

    'summary': """
        Short (1 phrase/line) summary of the module's purpose, used as
        subtitle on modules listing or apps.openerp.com""",

    'description': """
        Long description of module's purpose
    """,

    'author': "SUDO",
    'website': "https://sudo.inc",
    'category': 'Uncategorized',
    'version': '0.1',
    'depends': ['base', 'mail'],

    'data': [
        'security/ir.model.access.csv',
        'security/incident_security.xml',
        'data/sequence.xml',
        'views/incident_main_views.xml',
        'views/sudo_category.xml',
        'views/sudo_affected_ci.xml',
        'views/incident_services.xml',
        'data/sequence.xml',
        # 'views/incident_manager_security.xml',
        # 'views/templates.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
