# -*- coding: utf-8 -*-
import json

from odoo import models, fields, api, _
from datetime import datetime


class SudoIncidentConfiguration(models.Model):
    _name = 'sudo_incident.configuration'
    _description = 'Incident Configuration'

    priority1 = fields.Integer('Priority 1:', default=120, readonly=True)
    priority2 = fields.Integer('Priority 2:', default=240, readonly=True)
    priority3 = fields.Integer('Priority 3:', default=360, readonly=True)
    priority4 = fields.Integer('Priority 4:', default=480, readonly=True)
