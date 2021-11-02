# -*- coding: utf-8 -*-
import json

from odoo import models, fields, api, _
from datetime import datetime


class SudoIncidentTags(models.Model):
    _name = 'sudo_incident.tags'
    _description = 'Sudo Incident tags'

    name = fields.Char('Incident Tags')