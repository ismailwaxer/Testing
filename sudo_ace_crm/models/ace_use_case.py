from odoo import models, fields, api


class SudoAceUseCase(models.Model):
    _name = 'ace.usecase'
    _rec_name = 'name'

    name = fields.Char(string='Use Case')