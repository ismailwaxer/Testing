# -*- coding: utf-8 -*-
import json

from odoo import models, fields, api, _
from datetime import datetime


class SudoWebHook(models.Model):
    _name = 'sudo_incident.webhook'
    _description = 'Sudo WebHook Configuration'

    name = fields.Char(string='Name')
    webhook_url = fields.Char(string='Webhook Url')