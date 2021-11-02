# -*- coding: utf-8 -*-
from odoo import models, fields, api


class SudoIncidentManagment(models.Model):
    _inherit = 'sudo_incident.sudo_incident'

    helpdesk_ticket_id = fields.Many2one(comodel_name="helpdesk.ticket", string="Helpdesk Ticket", required=False)


class HelpdeskInherit(models.Model):
    _inherit = 'helpdesk.ticket'

    incident_count = fields.Integer(compute='compute_count')

    def sudo_incident_select(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Incident',
            'view_mode': 'tree,form',
            'res_model': 'sudo_incident.sudo_incident',
            'domain': [('helpdesk_ticket_id', '=', self.id)],
            'context': "{'create': False}"
        }

    def compute_count(self):
        for record in self:
            record.incident_count = self.env['sudo_incident.sudo_incident'].search_count(
                [('helpdesk_ticket_id', '=', self.id)])

    def incident_create(self):
        rc = self.env['helpdesk.ticket'].search([('id','=',self.id)])
        for i in rc:
            ctx = {
                'default_model': 'sudo_incident.sudo_incident',
                'default_title': i.display_name,
                'default_description': i.description,
                'default_helpdesk_ticket_id': i.id,
                'default_partner_id': i.partner_id.id,
            }
        return {
            'name': "Incident Create",
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'sudo_incident.sudo_incident',
            'view_id': self.env.ref('sudo_incident.sudo_incident_form_id').id,
            'target': 'new',
            'context': ctx,
        }


