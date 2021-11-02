# -*- coding: utf-8 -*-


from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
from datetime import time


class IncidentMergeWizard(models.TransientModel):
    _name = "incident.merge.wizard"
    _description = 'Helpdesk Ticket Merge Wizard'

    merge_incident_line_ids = fields.One2many(
        'merge.incident.line',
        'primary_incident_merge_id',
        string="Merge Ticket Line",
        readonly=True,
    )

    support_incident_id = fields.Many2one(
        'sudo_incident.sudo_incident',
        string="Set as Primary Incident",
    )
    current_user = fields.Many2one(
        'res.users',
        string='Responsible User',
        required=True,
    )

    create_new_incident = fields.Boolean(
        string='Create New Incident?'
    )
    incident_subject = fields.Char(
        string='Subject'
    )
    primary_id = fields.Many2one(
        'sudo_incident.sudo_incident',
        string="Primary Incident",
    )
    merge_ids = fields.Many2many(
        'sudo_incident.sudo_incident',
        string="Merge Incident",
    )
    is_sure = fields.Boolean(
        string="Are You Sure ?",
    )
    merge_reason = fields.Char(
        string="Merge Reason",
        required=True,
    )
    partner_id = fields.Many2one(
        'res.partner',
        string='Customer'
    )  # ent_13
    description = fields.Text(
        string='Description'
    )
    title = fields.Char(
        string='Title'
    )

    helpdesk_ticket_id = fields.Many2one(
        'helpdesk.ticket',
        string="Helpdesk Ticket"
    )
    sla_branches_in = fields.Integer(string='SLA Breaches In:', required=True, tracking=True)
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
        string='Status:', required=True, tracking=True,
    )

    incident_tag_new = fields.Many2many(
        'sudo_incident.tags',
        string='Tags'
    )

    @api.model
    def default_get(self, fields):
        res = super(IncidentMergeWizard, self).default_get(fields)
        incident_obj = self.env['sudo_incident.sudo_incident']
        incident_ids = incident_obj.search(
            [('id', 'in', self._context.get('active_ids'))]
        )
        incident_line = self.env['merge.incident.line']
        if all([x.partner_id.commercial_partner_id in incident_ids[0].partner_id.commercial_partner_id
                for x in incident_ids]):
            if 'merge_incident_line_ids' in fields:

                tags = []
                for incident in incident_ids:
                    vals = {
                        'ticket_id': incident.id,
                        'title': incident.title,
                        'subject': incident.display_name,
                    }
                    incident_line += incident_line.create(vals)
                    if incident.incident_tag_new:
                        tags.extend(incident.incident_tag_new.ids)
                        tags = list(set(tags))
                res.update({
                    'merge_incident_line_ids': [(6, 0, incident_line.ids)],
                    'merge_ids': [(6, 0, incident_ids.ids)],
                    'current_user': incident.current_user,
                    'partner_id': incident.partner_id.id,
                    'description': incident.description,
                    'status': incident.status,
                    'sla_branches_in': incident.sla_branches_in,
                    'title': incident.title,
                    'helpdesk_ticket_id': incident.helpdesk_ticket_id,
                    'incident_tag_new': [(6, 0, tags)],
                })
        else:
            raise ValidationError(_("Must be Same Partner or Email or Phone."))
        return res

    # @api.multi
    def action_merge_incident(self):
        context = dict(self._context or {})
        active_ids = context.get('active_ids', [])
        desc = ''
        helpdesk_support_obj = self.env['sudo_incident.sudo_incident']
        primary_ticket = self.primary_id
        if self.primary_id:
            if self.is_sure:
                primary_ticket.write({'is_secondry': True})
                for line in self.merge_ids:
                    if line == self.primary_id:
                        pass
                    else:
                        merge_ticket = line
                        d = merge_ticket.description or ''
                        desc += '\n' + d
                        merge_ticket.write({
                            'primary_ticket_id': primary_ticket.id,
                            'is_secondry': True,
                            'active': False,
                        })
                primary_ticket.write({
                    'description': self.primary_id.description or '' + desc,
                    'merge_reason': self.merge_reason,
                })
                res = self.env.ref('sudo_incident.sudo_incident_action_window')
                res = res.read()[0]
                res['domain'] = str([('id', '=', primary_ticket.id)])
                return res
            else:
                raise ValidationError(_("Please select check box to confirm merge."))
        if self.create_new_incident:
            add_desc = ''
            for line in self.merge_ids:
                add_desc += '\n' + (line.description or '')
            if self.is_sure:  # ent_13
                tags = []
                tags.extend(self.incident_tag_new.ids)
                tags = list(set(tags))
                new_ticket_vals = {
                    'title': self.title,
                    'status': self.status,
                    'sla_branches_in': self.sla_branches_in,
                    'current_user': self.current_user.id,
                    'merge_reason': self.merge_reason,
                    'description': add_desc,
                    'partner_id': self.partner_id.id,
                    'incident_tag_new': [(6, 0, tags)],
                }
                new_ticket = helpdesk_support_obj.create(new_ticket_vals)
                self.merge_ids.write({
                    'active': False
                })
            else:
                raise ValidationError(_("Please select check box to confirm create."))  # ent_13


class MergeIncidentLine(models.TransientModel):
    _name = "merge.incident.line"
    _description = 'Merge Incident Line'

    ticket_id = fields.Many2one('sudo_incident.sudo_incident',string="Support Incident",readonly=True,)

    subject = fields.Text( string='Subject',)
    primary_incident_merge_id = fields.Many2one('incident.merge.wizard',string="Merge",)
    current_user = fields.Many2one('res.users',string='Responsible User',related='ticket_id.current_user',)
    partner_id = fields.Many2one('res.partner',string='Customer',related='ticket_id.partner_id',)
    description = fields.Text(string='Description',related='ticket_id.description',)
    title = fields.Char(string='Title',related='ticket_id.title')
    sla_branches_in = fields.Integer(string='SLA Breaches In:', tracking=True)
    status = fields.Selection([
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
        string='Status:', tracking=True,
        related='ticket_id.status')

    helpdesk_ticket_id = fields.Many2one('helpdesk.ticket',string='Helpdesk Ticket',related='ticket_id.helpdesk_ticket_id',)
    incident_tag_new = fields.Many2many('sudo_incident.tags',string='Tags',related='ticket_id.incident_tag_new',)
