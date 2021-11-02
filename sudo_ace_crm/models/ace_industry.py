from odoo import models, fields, api


class SudoAceConfigIndustry(models.Model):
    _name = 'ace.industry'
    _rec_name = 'name'

    name = fields.Char(string='Industry')