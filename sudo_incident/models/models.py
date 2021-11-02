from odoo import models, fields, api, _, modules, tools, exceptions
from odoo.exceptions import ValidationError, UserError
import logging
from datetime import timedelta, datetime
from werkzeug.urls import url_encode

import requests
import json
import time
import datetime
from odoo.http import request
from odoo.tools.misc import get_lang
from lxml import etree
import base64

_logger = logging.getLogger(__name__)


class SudoIncidentMain(models.Model):
    _name = 'sudo_incident.sudo_incident'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    # _inherits = ['ir.actions.server']
    _description = 'Incident'
    _rec_name = 'title'

    title = fields.Char(string='Title:', required=True, tracking=True, )
    sla_branches_in = fields.Integer(string='SLA Breaches In:')
    description = fields.Text(string='Description:', required=True, tracking=True)
    incident_id = fields.Char(string='Incident ID:', tracking=True, required=True, copy=False, readonly=True,
                              index=True, default=lambda self: _('New'))
    active = fields.Boolean(default=True)
    status = fields.Selection(
        [
            ('categorize', 'Categorize'),
            ('assig', 'Assign'),
            ('work in progress', 'Work In Progress'),
            ('pending vendor', 'Pending vendor'),
            ('pending customer', 'Pending customer'),
            ('pending evidence', 'Pending Evidence'),
            ('pending other', 'Pending Other'),
            ('resolved', 'Resolved'),
            ('closed', 'Closed'),
        ],
        string='Status:', default='categorize', tracking=True)
    phase = fields.Selection(
        [
            ('logging', 'Logging'),
            ('categorize', 'Categorization'),
            ('investigation', 'Investigation'),
            ('recovery', 'Recovery'),
            ('review', 'Review'),
            ('closure', 'Closure'),
        ],
        string='Phase:', tracking=True)
    partner_id = fields.Many2one('res.partner', tracking=True, required="True", string="Affected Customer:", index=True)
    affected_service = fields.Many2one('sudo_incident.service', string="Affected Services:", index=True)
    affected_subservice = fields.Many2one('sudo_incident.service', string="Affected Sub services")
    outage_start_time = fields.Datetime(string="Outage Start Time:", default=lambda self: fields.datetime.now(),
                                        tracking=True)
    outage_end_time = fields.Datetime(string='Outage End Time:', tracking=True)
    cause_code = fields.Many2one('sudo_incident.cause_code', srting='Cause Code', tracking=True)
    major_incident = fields.Boolean(string='Major Incident:', readonly=True, tracking=True)
    o_is = fields.Boolean(string='O Is Optional(no outage):', tracking=True)
    escalated = fields.Boolean(string='Escalated', readonly=True, tracking=True)
    proactive = fields.Boolean(string='Proactive', tracking=True)
    incident_last_status = fields.Text(string='Incident Last Status:', tracking=True)
    category_list = fields.Many2one(comodel_name="sudo_incident.category", string="Category:", required=False, )
    sub_category = fields.Many2one(comodel_name="sudo_incident.category", string=" Child Category:", required=False, )

    folder = fields.Selection(
        [('1 folder', '1-folder'), ('2 folder', '2-folder'), ('3 folder', '3-folder'),
         ('4 folder', '4-folder')], string='Folder:', tracking=True)

    opened_by = fields.Char(string='Opened By:', default=lambda self: self.env.user.name, required=True, tracking=True)
    request_impact = fields.Selection(string="Impact:", selection=[
        ('minor', 'Minor'),
        ('moderate', 'Moderate'),
        ('significant', 'Significant'),
        ('extensive', 'Extensive'),
    ], default='minor', help="Priority depend on Impact and Urgency", tracking=True)

    request_type = fields.Selection(string="Urgency", selection=[
        ('standard', 'Standard Change (Low)'),
        ('minor', 'Minor Change (Medium)'),
        ('major', 'Major Change (High)'),
        ('emergency', 'Emergency Change (Urgent)'),
    ], default='standard', help="Priority depend on Impact and Urgency", tracking=True)

    priority = fields.Integer(compute='_compute_priority', tracking=True)
    assign_group = fields.Selection(string="Assign Group:", selection=[
        ('l1', 'L1'),
        ('l2', 'L2'), ], tracking=True)
    current_user = fields.Many2one('res.users', default=lambda self: self.env.uid, string='Assigned to', tracking=True)
    incident_tag_new = fields.Many2many(comodel_name="sudo_incident.tags",
                                        string='Tags:', tracking=True)
    email_sent = fields.Boolean('Email Sent', default=False)
    check = fields.Boolean('Check', default=False)
    image = fields.Image()
    proposed_solution = fields.Text(string="Proposed Solution", tracking=True)

    priority_1 = fields.Integer('Priority 1:', default=120, readonly=True)

    # priority_1 = fields.Datetime('Priority 1:')
    priority_2 = fields.Integer('Priority 2:', default=240, readonly=True)
    priority_3 = fields.Integer('Priority 3:', default=360, readonly=True)
    priority_4 = fields.Integer('Priority 4:', default=480, readonly=True)

    # <------- Cron job for sla breaches---------->
    def test_cron_sls(self):
        main = self.env['sudo_incident.sudo_incident'].sudo().search([])
        for record in main:
            if int(record.priority) == 1:
                created_date_time = record.outage_start_time
                current_time = datetime.datetime.now()
                timedelta = (created_date_time - current_time)
                total_seconds = timedelta.total_seconds()
                minute = total_seconds / 60
                d = abs(minute)
                calculate_priority = record.priority_1 - d
                if calculate_priority >= 0:
                    record.sla_branches_in = calculate_priority
                else:
                    break
            elif int(record.priority) == 2:
                created_date_time = record.outage_start_time
                current_time = datetime.datetime.now()
                timedelta = (created_date_time - current_time)
                total_seconds = timedelta.total_seconds()
                minute = total_seconds / 60
                d = abs(minute)
                calculate_priority = record.priority_2 - d
                if calculate_priority >= 0:
                    record.sla_branches_in = calculate_priority
                # record.sla_branches_in = calculate_priority
                #     # record.write({'sla_branches_in': calculate_priority})
                else:
                    break
            elif int(record.priority) == 3:
                created_date_time = record.outage_start_time
                current_time = datetime.datetime.now()
                timedelta = (created_date_time - current_time)
                total_seconds = timedelta.total_seconds()
                minute = total_seconds / 60
                d = abs(minute)
                calculate_priority = record.priority_3 - d
                if calculate_priority >= 0:
                    record.sla_branches_in = calculate_priority
                # record.sla_branches_in = calculate_priority
                #     # record.write({'sla_branches_in': calculate_priority})
                else:
                    break
            elif int(record.priority) == 4:
                created_date_time = record.outage_start_time
                current_time = datetime.datetime.now()
                timedelta = (created_date_time - current_time)
                total_seconds = timedelta.total_seconds()
                minute = total_seconds / 60
                d = abs(minute)
                calculate_priority = record.priority_4 - d
                if calculate_priority >= 0:
                    record.sla_branches_in = calculate_priority
                # record.sla_branches_in = calculate_priority
                #     # record.write({'sla_branches_in': calculate_priority})
                else:
                    break
        return main

    # <------- WorkFlow images ---------->
    @api.onchange('status')
    def _onchange_status(self):
        for rec in self:
            if rec.status == 'categorize':
                image_path = modules.get_module_resource('sudo_incident', 'static/src/image', 'category.jpeg')
                rec.image = base64.b64encode(open(image_path, 'rb').read())

            elif rec.status == 'assig':
                image_path = modules.get_module_resource('sudo_incident', 'static/src/image', 'assign.jpeg')
                rec.image = base64.b64encode(open(image_path, 'rb').read())
            elif rec.status == 'work in progress':
                image_path = modules.get_module_resource('sudo_incident', 'static/src/image', 'work in progress.jpeg')
                rec.image = base64.b64encode(open(image_path, 'rb').read())
            elif rec.status == 'pending vendor':
                image_path = modules.get_module_resource('sudo_incident', 'static/src/image', 'pending vendor.jpeg')
                rec.image = base64.b64encode(open(image_path, 'rb').read())
            elif rec.status == 'pending customer':
                image_path = modules.get_module_resource('sudo_incident', 'static/src/image', 'pending customer.jpeg')
                rec.image = base64.b64encode(open(image_path, 'rb').read())
            elif rec.status == 'pending evidence':
                image_path = modules.get_module_resource('sudo_incident', 'static/src/image', 'pending evidence.jpeg')
                rec.image = base64.b64encode(open(image_path, 'rb').read())
            elif rec.status == 'pending other':
                image_path = modules.get_module_resource('sudo_incident', 'static/src/image', 'pending other.jpeg')
                rec.image = base64.b64encode(open(image_path, 'rb').read())
            elif rec.status == 'resolved':
                image_path = modules.get_module_resource('sudo_incident', 'static/src/image', 'resolved.jpeg')
                rec.image = base64.b64encode(open(image_path, 'rb').read())
            elif rec.status == 'closed':
                image_path = modules.get_module_resource('sudo_incident', 'static/src/image', 'closed.jpeg')
                rec.image = base64.b64encode(open(image_path, 'rb').read())

    def get_values_id(self):
        all_category = self.env['sudo_incident.category'].search([])
        parent_list = []
        for rec in all_category:
            if rec.parent_id:
                parent_list.append((str(rec.id), rec.parent_id.name))
        return parent_list

    # <-------- incident services change on status field ----------->
    @api.onchange('partner_id')
    def _onchange_affected_services(self):
        affect = self.env['sudo_incident.service'].search([('services_parent', '!=', False)])
        list = []
        for i in affect:
            list.append(
                i.services
            )
        return {'domain': {'services': [('id', '=', list)]}}

    @api.onchange('affected_service')
    def _onchange_affected_sub(self):
        affect_service_new = self.affected_service
        affect_service_child = affect_service_new.serviceschild_ids.ids
        return {'domain': {'affected_subservice': [('id', '=', affect_service_child)]}}

    # <-------- category list depend on status field ------->
    @api.onchange('partner_id')
    def _onchange_category_list(self):
        category_e = self.env['sudo_incident.category'].search([('parent_id', '!=', False)])
        list = []
        for i in category_e:
            list.append(i.name)
        return {'domain': {'name': [('id', '=', list)]}}

    @api.onchange('category_list')
    def _onchange_category_sub(self):
        category_parent = self.category_list
        category_child_new = category_parent.child_ids.ids
        return {'domain': {'sub_category': [('id', '=', category_child_new)]}}


    @api.depends('request_type', 'request_impact')
    def _compute_priority(self):
        for record in self:
            if (record.request_type == "emergency" and record.request_impact == "extensive") or \
                    (record.request_type == "emergency" and record.request_impact == "significant") or \
                    (record.request_type == "major" and record.request_impact == "extensive"):
                record.priority = 1
                record.check = True
                record.test_cron_sls()
            elif (record.request_type == "minor" and record.request_impact == "extensive") or \
                    (record.request_type == "major" and record.request_impact == "significant") or \
                    (record.request_type == "emergency" and record.request_impact == "moderate") or \
                    (record.request_type == "major" and record.request_impact == "moderate") or \
                    (record.request_type == "emergency" and record.request_impact == "minor"):
                record.priority = 2
                record.check = True
                record.test_cron_sls()
            elif (record.request_type == "minor" and record.request_impact == "significant") or \
                    (record.request_type == "minor" and record.request_impact == "moderate") or \
                    (record.request_type == "major" and record.request_impact == "minor") or \
                    (record.request_type == "minor" and record.request_impact == "minor"):
                record.priority = 3
                record.check = False
                record.test_cron_sls()

            else:
                record.priority = 4
                record.check = False
                record.test_cron_sls()

    @api.model
    def create(self, vals):
        if vals.get('incident_id', _('New')) == _('New'):
            vals['incident_id'] = self.env['ir.sequence'].next_by_code('sudo.si_incident') or _('New')
            result = super(SudoIncidentMain, self).create(vals)
        self.mail_reminder()
        return result

    def write(self, vals):
        """
               Edit incident and then send email to user
        """
        if 'current_user' in vals and self.ids:
            user_group = self.env.ref("sudo_incident.incident_manager_security")
            email_list = [usr.partner_id.email for usr in user_group.users if usr.partner_id.email]

            user_group_l1 = self.env.ref("sudo_incident.incident_group_l1_security")
            email_group_l1 = [usr.partner_id.email for usr in user_group_l1.users if usr.partner_id.email]

            log = self.current_user.login
            all_eamils = [log, email_list, email_group_l1]
            template_rec = self.env.ref('sudo_incident.mail_template_sudo_incident_mail')
            template_rec.write({'email_to': all_eamils})
            template_rec.send_mail(self.id, force_send=True)
        return super(SudoIncidentMain, self).write(vals)

    @api.model
    def message_new(self, msg_dict, custom_values=None):
        """
        Creates new Incident from emails
        """
        title = msg_dict.get('subject', '')
        email_from = msg_dict.get('email_from', '')
        email_body = msg_dict.get('body', '')
        description = "Mail From: %s\n\nDescription:\n%s" % (email_from, email_body)
        to_email = msg_dict.get('to', 'unknown email')
        if custom_values is None:
            custom_values = {}
        defaults = {
            'title': title,
            'description': description,
            'opened_by': to_email
        }
        defaults.update(custom_values)

        return super(SudoIncidentMain, self).message_new(msg_dict, defaults)

    # <!------- Email Notification ---------->
    def mail_reminder(self):

        assign_to_user = self.env['sudo_incident.sudo_incident'].search([('email_sent', '=', False)])
        for rec in assign_to_user:
            if rec.email_sent is False:
                rec.mail_reminder_abc()
                rec.email_sent = True

    def mail_reminder_abc(self):

        user_group = self.env.ref("sudo_incident.incident_manager_security")
        email_group_manager = [usr.partner_id.email for usr in user_group.users if usr.partner_id.email]

        user_group_l1 = self.env.ref("sudo_incident.incident_group_l1_security")
        email_group_l1 = [usr.partner_id.email for usr in user_group_l1.users if usr.partner_id.email]

        user_group_l2 = self.env.ref("sudo_incident.incident_group_l2_security")
        email_group_l2 = [usr.partner_id.email for usr in user_group_l2.users if usr.partner_id.email]

        log = self.current_user.login
        all_eamils = [log, email_group_l2, email_group_manager, email_group_l1]
        for email in all_eamils:
            template_rec = self.env.ref('sudo_incident.mail_template_sudo_incident_mail')
            template_rec.write({'email_to': email})
            template_rec.send_mail(self.id, force_send=True)

    # <!--------- End of Email Notification --------->
    @api.model
    def get_full_url(self):
        """
         this function is work when email send to user, in email template there is button view incident when
         click on this button this function is working.
       """
        self.ensure_one()
        base_url = self.env["ir.config_parameter"].sudo().get_param("web.base.url")
        url_params = {
            'id': self.id,
            'view_type': 'form',
            'model': 'sudo_incident.sudo_incident',
            'menu_id': self.env.ref('sudo_incident.sudo_incident_menu').id,
            'action': self.env.ref('sudo_incident.sudo_incident_action_window').id,
        }
        params = '/web?#%s' % url_encode(url_params)

        return base_url + params

    @api.onchange('assign_group')
    def onchange_current_user(self):
        """
             This Function works as domain for current_user field this will show only those users which have the
             the group selected in the assign_group selection field, base on security
        """
        for rec in self:
            if rec.assign_group == 'l1':
                users = self.env.ref('sudo_incident.incident_group_l1_security').users.ids
                return {'domain': {'current_user': [('id', 'in', users)]}}
            else:
                users = self.env.ref('sudo_incident.incident_group_l2_security').users.ids
                return {'domain': {'current_user': [('id', 'in', users)]}}

    @api.onchange('major_incident')
    def _onchange_major_incident(self):
        webhook = self.env['sudo_incident.webhook'].sudo().search([('name', '=', 'major incident')])
        for rec in webhook:
            web_hook_url = rec.webhook_url

        for record in self:
            import urllib
            details = "ID: %s\nImpact: %s\nUrgency: %s\nPriority: %s" % (
                record.incident_id, record.request_impact, record.request_type, record.priority)
            details = urllib.parse.quote_plus(details)
            if record.major_incident == False:
                return {}
            if record.incident_id == "New":
                warning_mess = {
                    'title': _('Cannot save before major Incident'),
                    'message': 'First save the incident then Major Incident'
                }
                record.major_incident = False
                return {'warning': warning_mess}
            webhook_url = str(web_hook_url) + "?summary=%s&details=%s&dedup=%s" % (
                record.title, details, record.incident_id)
            data = {
            }
            requests.post(webhook_url, data=json.dumps(data), headers={'Content-Type': 'application/json'})

    # <------- Incident Assign to Me Function ---------->
    def assign_incident_to_self(self):
        self.ensure_one()
        self.current_user = self.env.user

    # <------- Incident Assign to Group L1 ---------->
    def assign_incident_to_l1(self):
        self.assign_group = 'l1'
        # self.mail_reminder()
        if self.assign_group == 'l1':
            # if self.current_user == self.env.user:
            user_group_l1 = self.env.ref("sudo_incident.incident_group_l1_security")
            email_group_l1 = [usr.partner_id.email for usr in user_group_l1.users if usr.partner_id.email]
            all_eamils = [email_group_l1]
            for email in all_eamils:
                template_rec = self.env.ref('sudo_incident.mail_template_sudo_incident_mail')
                template_rec.write({'email_to': email})
                template_rec.send_mail(self.id, force_send=True)

    def closed_to_cr(self):
        pass
