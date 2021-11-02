from odoo import models, fields, api


class SudoAceUseSubCase(models.Model):
    _name = 'ace.subusecase'
    _rec_name = 'name'

    name = fields.Char(string='Sub Use Case')
    case_id = fields.Many2one('ace.usecase', 'Use Case')