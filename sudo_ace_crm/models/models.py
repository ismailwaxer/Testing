# -*- coding: utf-8 -*-

from odoo import models, fields, api, exceptions, _
from odoo.exceptions import ValidationError


class SudoAceCrm(models.Model):
    _inherit = 'crm.lead'

    submit_to_AWS = fields.Selection([
        ('Yes', 'Yes'),
        ('No', 'No'),],
        string='Submit to AWS', default='No',required=True)

    industry_new = fields.Many2one('ace.industry', string='Industry')
    usecase = fields.Many2one('ace.usecase', string='Use Case')
    sub_usecase = fields.Many2one('ace.subusecase', string='Sub Use Case')
    country_name = fields.Char("Country Name")

    partner_project_title = fields.Char(string='Partner Project Title', )
    project_description = fields.Text(string='Project Description', )

    partner_primary_need_from_aws = fields.Selection([
        ('Architectural validation', 'Architectural validation'),
        ('Business presentation', 'Business presentation'),
        ('Competitive Information', 'Competitive Information'),
        ('Pricing Assistance', 'Pricing Assistance'),
        ('Technical consultation', 'Technical consultation'),
        ('Total Cost of Ownership Evaluation', 'Total Cost of Ownership Evaluation'),
        ('For Visibility - No Assistance Needed', 'For Visibility - No Assistance Needed'),
        ('Deal support', 'Deal support'),
        ('Other', 'Other'),
    ], string='Partner Primary Need From Aws', )

    currency_id = fields.Many2one('res.currency', string='Currency')

    expected_monthly_aws_revenue = fields.Monetary(string='Expected Monthly AwsRevenue', )
    target_close_date = fields.Date(string='Target CloseDate', )
    aWSCloseDate = fields.Date(string='Aws Close Date', )

    delivery_model = fields.Selection([
        ('SaaS or PaaS', 'SaaS or PaaS'),
        ('BYOL or AMI', 'BYOL or AMI'),
        ('Managed Services', 'Managed Services'),
        ('Professional Services', 'Professional Services'),
        ('Resell', 'Resell'),
        ('Other', 'Other'),

    ], string='Delivery Model', )

    opportunity_owner_name = fields.Char(string='Opportunity Owner Name', )
    opportunity_owner_email = fields.Char(string='Opportunity Owner Email', )

    isnet_newbusiness_forcompany = fields.Selection([
        ('Yes', 'Yes'),
        ('No', 'No'),

    ], string='isNetNewBusinessForCompany', )

    status = fields.Selection([
        ('Draft', 'Draft'),
        ('Submitted', 'Submitted'),
        ('In review', 'In review'),
        ('Approved', 'Approved'),
        ('Rejected', 'Rejected'),
        ('Action Required', 'Action Required'),

    ], string='Status', )

    contract_vehicle = fields.Char(string='Contract Vehicle', )

    closed_lost_reason = fields.Selection([
        ('Customer Deficiency', 'Customer Deficiency'),
        ('Delay / Cancellation of Project', 'Delay / Cancellation of Project'),
        ('Legal / Tax / Regulatory', 'Legal / Tax / Regulatory'),
        ('Lost to Competitor – Google', 'Lost to Competitor – Google'),
        ('Lost to Competitor – Microsoft', 'Lost to Competitor – Microsoft'),
        ('Lost to Competitor – SoftLayer', 'Lost to Competitor – SoftLayer'),
        ('Lost to Competitor – VMWare', 'Lost to Competitor – VMWare'),
        ('Lost to Competitor – Other', 'Lost to Competitor – Other'),
        ('No Opportunity', 'No Opportunity'),
        ('On Premises Deployment', 'On Premises Deployment'),
        ('Partner Gap', 'Partner Gap'),
        ('Price', 'Price'),
        ('Security / Compliance', 'Security / Compliance'),
        ('Technical Limitations', 'Technical Limitations'),
        ('Customer Experience', 'Customer Experience'),
        ('Other', 'Other'),
        ('People/Relationship/Governance', 'People/Relationship/Governance'),
        ('Product/Technology', 'Product/Technology'),

    ], string='Closed Lost Reason', )

    aws_field_engagement = fields.Selection([
        ('Yes', 'Yes'),
        ('No', 'No'),

    ], string='Aws Field Engagement', )

    stage = fields.Selection([
        ('Prospect', 'Prospect'),
        ('Qualified', 'Qualified'),
        ('Technical Validation', 'Technical Validation'),
        ('Business Validation', 'Business Validation'),
        ('Committed', 'Committed'),
        ('Launched', 'Launched'),
        ('Closed Lost', 'Closed Lost'),
    ], string='Stage')

    next_step = fields.Char(string='Next Step')
    apn_crmunique_identifier = fields.Char(string='Apn CrmUnique Identifier')
    partner_crmunique_identifier = fields.Char(string='Partner CrmUnique Identifier')
    aws_account_id = fields.Char(string='AWS Account Id', default='00')

    opportunity_ownership = fields.Selection([
        ('AWS Referral', 'AWS Referral'),
        ('Partner Referral', 'Partner Referral'),
    ], string='Opportunity Ownership', )

    isthis_apublic_reference = fields.Selection([
        ('Yes', 'Yes'),
        ('No', 'No'),

    ], string='is This APublic Reference', )

    is_this_for_resell = fields.Selection([
        ('Yes', 'Yes'),
        ('No', 'No'),

    ], string='is This APublic Reference', )

    public_referenceUrl = fields.Char(string='Public ReferenceUrl', )
    customer_website = fields.Char(string='Customer Website')

    partner_primary_needfromAwsOther = fields.Char(string='Partner Primary Need From Aws Other', )
    partner_developer_managerPhone = fields.Char(string='Partner Developer Manager Phone', )
    partner_developer_manager_email = fields.Char(string='Partner Developer Manager Email', )
    partnerDeveloperManager = fields.Char(string='Partner Developer Manager', )
    next_step_history = fields.Text(string='Next Step History', )

    public_referenceTitle = fields.Char(string='Public Reference Title', )

    is_this_for_marketplace = fields.Selection([
        ('Yes', 'Yes'),
        ('No', 'No'), ], string='Is This For Market Place')

    isMarketingDevelopmentFunded = fields.Selection([
        ('Yes', 'Yes'),
        ('No', 'No'), ],
        string='isMarketing DevelopmentFunded',
    )
    industryothers = fields.Char(string='Industry Other')

    partner_acceptance_status = fields.Selection([
        ('Accepted', 'Accepted'),
        ('Rejected', 'Rejected'), ],
        string='Partner Acceptance Status')

    competitive_tracking = fields.Selection([
        ('Oracle Cloud', 'Oracle Cloud'),
        ('On-Prem', 'On-Prem'),
        ('Co-location', 'Co-location'),
        ('Akamai', 'Akamai'),
        ('AliCloud', 'AliCloud'),
        ('Google Cloud Platform', 'Google Cloud Platform'),
        ('IBM Softlayer', 'IBM Softlayer'),
        ('Microsoft Azure', 'Microsoft Azure'),
        ('Other- Cost Optimization', 'Other- Cost Optimization'),
        ('No Competition', 'No Competition'),
        ('*Other', '*Other'),
    ], string='Competitive Tracking', )

    competitiveTrackingOther = fields.Char(string='Competitive Tracking Other', )
    aws_stage = fields.Char(string='Aws Stage', )
    aws_sales_RepName = fields.Char(string='Aws Sales RepName', )
    aws_sales_repEmail = fields.Char(string='Aws Sales RepEmail', )
    aws_partner_success_manager_name = fields.Char(string='aWSPartnerSuccessManagerName', )

    awsPartnerSuccessManagerEmail = fields.Char(string='Aws Partner Success Manager Email', )
    awsISVSuccessManagerName = fields.Char(string='Aws ISV Success Manager Name', )
    awsISVSuccessManagerEmail = fields.Char(string='Aws ISV Success Manager Email', )
    awsAccountOwnerName = fields.Char(string='Aws Account Owner Name', )

    awsAccountOwnerEmail = fields.Char(string='Aws Account Owner Email', )
    wWPSPDMEmail = fields.Char(string='wWPSPDM Email', )
    wwpspdm = fields.Char(string='wWPSPDM', )

    lead_source = fields.Char(string="Lead Source")
    current_lead_stage = fields.Selection([
        ('Accepted', 'Accepted'),
        ('Rejected', 'Rejected'),
    ], string='Current Lead Stage', )

    partner_crm_lead_id = fields.Integer(string="Partner Crm Lead Id")
    segment_company_size = fields.Char(string="Segment Company Size")
    level_of_aws_usage = fields.Char(string="Level of AWS Usage")
    lead_status_reason = fields.Char(string="lead Status Reason")

    campaign_member_status = fields.Char(string="Campaign Member Status")
    lead_age = fields.Integer(string="Lead Age")
    last_update_date = fields.Datetime("Last update date", default=fields.Datetime.now)
    sent_to_aws = fields.Boolean('Sent to Aws', default=True)
    from_ui = fields.Boolean('form ui')

    additionalComments = fields.Text(string="additionalComments")
    aws_last_modified_by = fields.Text(string="AWS last modified by")
    aws_last_modified_date = fields.Date(string="AWS last modified date")
    website_ids = fields.Char('Website', index=True,
                          help="Website of the contact",
                          compute="_compute_website", readonly=False, store=True
                          )

    @api.depends('partner_id')
    def _compute_website(self):
        """ compute the new values when partner_id has changed """
        for lead in self:
            if not lead.website_ids or lead.partner_id.website_id:
                lead.website_ids = lead.partner_id.website_id

    @api.onchange('country_id')
    def _onchange_country_id(self):
        for rec in self:
            rec.country_name = rec.country_id.name

    @api.onchange('usecase')
    def _onchange_use_case(self):
        my_list = []
        sub_use_case = self.env['ace.subusecase'].search([])
        for rec in sub_use_case:
            if self.usecase.id == rec.case_id.id:
                my_list.append(rec.id)

        return {'domain': {'sub_usecase': [('id', '=', my_list)]}}

    @api.constrains('aws_account_id')
    def _check_value(self):
        if len(self.aws_account_id) != 12:
            raise ValidationError(_('Enter Valid 12 digits Code of AWS Account id'))

    @api.constrains('expected_monthly_aws_revenue')
    def _check_expected_monthly_aws_revenue(self):
        if self.expected_monthly_aws_revenue <= 0:
            raise ValidationError(_('Enter 0+ Value of Expected Monthly AWs Revenue'))


    @api.model
    def create(self, vals_list):
        res = super(SudoAceCrm, self).create(vals_list)
        res['partner_crmunique_identifier'] = res['code']
        res['next_step_history'] = res['next_step']
        res['sent_to_aws'] = False
        return res

    # def write(self, vals):
    #     for rec in self:
    #         if rec.from_ui == False:
    #             vals['sent_to_aws'] = False
    #         elif rec.from_ui == True:
    #             vals['sent_to_aws'] = False
