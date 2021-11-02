# -*- coding: utf-8 -*-
import json
import logging
import re

from odoo import api, fields, models, tools, _
from odoo.exceptions import UserError, ValidationError
from odoo.osv import expression

from odoo.tools import float_compare

_logger = logging.getLogger(__name__)


class SudoIncidentService(models.Model):
    _name = 'sudo_incident.service'
    _description = 'Incident Service'
    _rec_name = 'complete_name'
    _order = 'complete_name'

    _parent_store = True
    _parent_name = "services_parent"

    services = fields.Char('Affected Services', index=True, required=True)

    # partner_id = fields.Many2one('res.partner', string="Cusotmer", index=True)

    complete_name = fields.Char(
        'Sudo Incident Services',compute='_compute_complete_name',
        store=True)

    services_parent = fields.Many2one(
        'sudo_incident.service',
        string='Parent Affected Services',
        ondelete='restrict',
        index=True
    )
    serviceschild_ids = fields.One2many(
        'sudo_incident.service', 'services_parent',
        string='Affected SubServices')

    parent_path = fields.Char(index=True)
    services_parent_domain = fields.Char(compute="_compute_services_parent_domain", readonly=True, store=False, )

    @api.depends('services_parent')
    def _compute_services_parent_domain(self):
        for rec in self:
            rec.services_parent_domain = json.dumps(
                [('services_parent', '=', rec.services_parent.id)]
            )

    @api.depends('services', 'services_parent.complete_name')
    def _compute_complete_name(self):
        for rec in self:
            if rec.services_parent:
                rec.complete_name = '%s / %s' % (rec.services_parent.complete_name, rec.services)
            else:
                rec.complete_name = rec.services

    @api.constrains('services_parent')
    def _check_hierarchy(self):
        if not self._check_recursion():
            raise models.ValidationError('Error! You cannot create recursive categories.')