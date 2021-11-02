# -*- coding: utf-8 -*-

from odoo import models, fields, api, _


class sudo_cmdb_datacneter(models.Model):
    pass

class sudo_cmdb_aws_datacneter(models.Model):
    pass


class sudo_cmdb_onprem_datacneter(models.Model):
    pass

class sudo_cmdb_aws_account(models.Model):
    pass

"account"
"ebs_encryption_settings"
"eip_address"
"image"
"instance"
"internet_gateway"
"network_acl"
"network_interface"
"route_table"
"security_group"
"snapshot"
"subnet"
"volume"
"vpc"

class sudo_cmdb_logical_datacneter(models.Model):
    _name = 'sudo.sudo_cmdb'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'SUDO CMDB main model'
    _rec_name = 'title'

    title = fields.Char(string='Title:', required=True, tracking=True)
    sla_branches_in = fields.Integer(string='SLA Branches In:', required=True, tracking=True)
    description = fields.Text(string='Description:', required=True, tracking=True)
    incident_id = fields.Char(string='Order Reference', required=True, copy=False, readonly=True,
                              index=True, default=lambda self: _('New'))
    # incident_id = fields.Char(string='Incident ID:', required=True, tracking=True)
    status = fields.Selection(
        [('assig', 'Assig'), ('work in progress', 'Work In Progress'), ('pending evidence', 'Pending Evidence'),
         ('pending other', 'Pending Other')], string='Status:', required=True, tracking=True)
    phase = fields.Char(srting='Phase:', tracking=True)
    # requested_by = fields.Char(string='Requested By:', required=True)
    # department = fields.Char(string='Department:', required=True)
    # mobile = fields.Integer(string='Mobile:', required=True)
    # email = fields.Char(string='Email:', required=True)
    # affected_service = fields.Many2many(comodel_name="ir.attachment", relation="m2m_ir_affected_service_contract_rel", column1="m2m_id",
    #                                column2="attachment_id", string='Affected Service:', required=True, tracking=True)

    affected_service = fields.Many2one('incident.service', string="Affected Services", index=True )
    affected_subservice = fields.Char('Affected SubServices', related='affected_service.services')



    # affected_id = fields.Selection(selection=lambda self: self.env['incident.affected'].get_result(),
    #                                string="Effected CI")
    # affected_id_file = fields.Many2many('ir.attachment', readonly=True)
    outage_start_time = fields.Datetime(string="Outage Start Time:", tracking=True)
    outage_end_time = fields.Datetime(string='Outage End Time:', tracking=True)
    cause_code = fields.Char(srting='Cause Code', required=True, tracking=True)
    # affected_ola = fields.Many2many(comodel_name="ir.attachment", relation="m2m_ir_affected_ola_rel", column1="m2m_id",
    #                                column2="attachment_id", string='Affected OLA:')
    # technology = fields.Selection([('assig', 'Assig'), ('work in progress', 'Work In Progress')], string='Technology')
    # affected_application = fields.Selection([('assig', 'Assig'), ('work in progress', 'Work In Progress')],
    #                                         string='Affected Application:')
    # time_spent = fields.Char(string='Time Spent (DD HH:MM:SS)')
    major_incident = fields.Boolean(string='Major Incident:', tracking=True)
    o_is = fields.Boolean(string='O Is Optional(no outage):', tracking=True)
    escalated = fields.Boolean(string='Escalated', required=True, tracking=True)
    proactive = fields.Boolean(string='Proactive', required=True, tracking=True)

    incident_last_status = fields.Text(string='Incident Last Status:', required=True, tracking=True)

    # category = fields.Char(string='Category:', required=True, tracking=True)
    category_list = fields.Many2one(comodel_name="sudo.category", string="Category", required=False, )
    # child_category = fields.Char('Child Category', related='category_list.name')
    child_category = fields.Many2one(comodel_name="sudo.category", string="Sub Category", required=False )
    folder = fields.Selection(
        [('1 folder', '1-folder'), ('2 folder', '2-folder'), ('3 folder', '3-folder'),
         ('4 folder', '4-folder')], string='Folder:', tracking=True)
    opened_by = fields.Char(string='Opened By', required=True, tracking=True)
    impact = fields.Selection(
        [('1 user', '1-User'), ('2 user', '2-User'), ('3 user', '3-User'),
         ('4 user', '4-User')], string='Impact:', required=True, tracking=True)
    urgency = fields.Selection(
        [('1 user', '1-User'), ('2 user', '2-User'), ('3 user', '3-User'),
         ('4 user', '4-User')], string='Urgency:', required=True, tracking=True)
    priority = fields.Selection(
        [('1 user', '1-User'), ('2 user', '2-User'), ('3 user', '3-User'),
         ('4 user', '4-User')], string='Priority:', required=True, tracking=True)

    sub_category = fields.Many2many(comodel_name="ir.attachment", relation="m2m_ir_sub_category_rell", column1="m2m_id",
                                    column2="attachment_id", string='Sub Category:', tracking=True)
    # area = fields.Many2many(comodel_name="ir.attachment", relation="m2m_ir_area_rel", column1="m2m_id",
    #                                 column2="attachment_id", string='Area:', tracking=True)
    odoo_group = fields.Many2many(comodel_name="ir.attachment", relation="m2m_ir_assignment_group_rel",
                                  column1="m2m_id",
                                  column2="attachment_id", string='Odoo Groups:', tracking=True)
    current_user = fields.Many2one('res.users','Odoo Internal User', default=lambda self: self.env.user)
    # incident_manager = fields.Many2many(comodel_name="ir.attachment", relation="m2m_ir_incident_manager_rel",
    #                                     column1="m2m_id",
    #                                     column2="attachment_id", string='Incident Manager:', tracking=True)

    incident_manager_2 = fields.Many2one('res.users', string='Incident Manager',
                                         domain=lambda self: self.check_for_manager())

    # odoo_tags_new = fields.Many2many(comodel_name="crm.lead", relation="m2m_ir_scope_new_tage_rel", column1="m2m_id",
    #                              column2="attachment_id_new", string='Odoo Tags:', tracking=True)

    odoo_tags_new = fields.Many2one('crm.tag', string='Odoo Tags:', )

    def check_for_manager(self):
        print("thois")
        print(self.env.context)

    def check_for_manager(self):
        all_user = self.env['res.users'].search([])
        user_list = []
        for rec in all_user:
            print(rec.user_has_groups('sudo_incident.incident_manager_security'))
            if rec.user_has_groups('sudo_incident.incident_manager_security'):
                user_list.append(rec)
            else:
                pass
        print(user_list)

    @api.model
    def create(self, vals):
        if vals.get('incident_id', _('New')) == _('New'):
            vals['incident_id'] = self.env['ir.sequence'].next_by_code('sudo.si_incident') or _('New')
            result = super(sudo_incident, self).create(vals)
        return result

    # @api.onchange('affected_id')
    # def _onchange_affected_id(self):
    #     for rec in self:
    #         all_affected_ci = self.env['incident.affected'].search([('id', '=', 3)])
    #         t = all_affected_ci.mapped('affected_id_new')
    #         print("Here is the t value", t.id)
        # p = self.env['sudo_incident.sudo_incident'].create({
        #     'affected_id_file':[(6,0,t)],
        # })
        # return p
        # self.affected_id_file.write()


class InheritIrAttachment(models.Model):
    _inherit = 'ir.attachment'

    partner_id = fields.Many2one('res.partner')
    product_id = fields.Many2one('product.product')

    # @api.onchange('affected_id')
    # def _onchange_affected_id(self):
    #     for rec in self:
    #         all_affected_ci = self.env['incident.affected'].search([('id', '=', 3)])
    #         t = all_affected_ci.mapped('affected_id_new')
    #         print("Here is the t value", t.id)
    # p = self.env['sudo_incident.sudo_incident'].create({
    #     'affected_id_file':[(6,0,t)],
    # })
    # return p
    # self.affected_id_file.write()
