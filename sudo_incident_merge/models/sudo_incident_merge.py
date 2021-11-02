# -*- coding: utf-8 -*-

# Part of Probuse Consulting Service Pvt Ltd.
#See LICENSE file for full copyright and licensing details.

from odoo import models, fields, api


class SudoIncidentMerge(models.Model):
    _inherit = "sudo_incident.sudo_incident"
    
    primary_ticket_id = fields.Many2one(
        'sudo_incident.sudo_incident',
        string="Primary Merge Incident",
    )
    merge_ticket_ids = fields.One2many(
        'sudo_incident.sudo_incident',
        'primary_ticket_id',
        string="Secondary Merge Incident",
    )
    is_secondry = fields.Boolean(
        string="Is Secondry ?",
        default=False,
    )
    merge_reason = fields.Char(
        string="Merge Reason",
    )

    #@api.multi
    def show_secondry_ticket(self):
        self.ensure_one()
        secondry = self.search([('primary_ticket_id', '=', self.id), ('active', '!=', True)])
        # res = self.env.ref('website_helpdesk_support_ticket.action_helpdesk_support')
        res = self.env.ref('sudo_incident.sudo_incident_action_window')
        res = res.read()[0]
        res['domain'] = str([('id', 'in', secondry.ids), ('active', '!=', True)])
        return res

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
