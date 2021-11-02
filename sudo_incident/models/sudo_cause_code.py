# -*- coding: utf-8 -*-

from odoo import models, fields, api, _


class SudoCauseCode(models.Model):
    _name = 'sudo_incident.cause_code'
    _description = 'Incident Cause Code'
    _rec_name = 'incident_code'

    incident_code = fields.Char(string="Incident Cause Code:")