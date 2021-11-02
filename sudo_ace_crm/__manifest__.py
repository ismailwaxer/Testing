# -*- coding: utf-8 -*-
{
    'name': "Sudo ACE Crm",

    'summary': """This module is design form add field to CRM""",

    'description': """This module is design form add field to CRM""",

    'author': "SUDO Consultants",
    'website': "https://sudoconsultants.com/",


    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'crm', 'crm_industry', 'crm_lead_code','crm_lead_firstname','partner_firstname'],

    # always loaded
    'data': [
        # 'data/ace.industry.csv',
        'data/ace.usecase.csv',
        'data/ace.subusecase.csv',
        'security/ir.model.access.csv',
        'views/ace_crm_main.xml',
        # 'views/aws_crm_main.xml',
        # 'views/ace_industry.xml',
        'views/ace_use_case.xml',
        'views/ace_sub_use_case.xml',
        'views/res_partner.xml',
        'views/templates.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
