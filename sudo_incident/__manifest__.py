# -*- coding: utf-8 -*-
{
    'name': "Incident Management",

    'summary': """Incident Management module to help you improve your services""",

    'description': """
        Incident Management is a process that is of getting your services back to operational as soon as possible without having a huge impact on your business, this module helps achieve this exact goal.
    """,

    'author': "SUDO Consultants",
    'website': "http://sudoconsultants.com",
    'price': 10,
    'currency': 'EUR',
    'category': 'Extra Tools',
    'version': '0.13',
    'depends': ['base', 'mail', 'web_domain_field'],

    'data': [
        'security/incident_security.xml',
        'data/incident_cron.xml',
        'data/sequence.xml',
        'security/ir.model.access.csv',
        'data/sequence.xml',
        'views/incident_main_views.xml',
        'views/sudo_category.xml',
        'views/incident_services.xml',
        'views/sudo_cause_code.xml',
        'views/sudo_configuration.xml',
        'views/incident_tags.xml',
        'views/sudo_webhook.xml',

    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
    'sequence': 1
}
