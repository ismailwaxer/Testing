# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import ValidationError


class SudoIncidentAffectedCi(models.Model):
    _name = 'incident.affected'
    _rec_name = 'name'

    name = fields.Char(string="Affected CI")




