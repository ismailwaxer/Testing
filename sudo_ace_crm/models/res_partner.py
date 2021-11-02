from odoo import models, fields, api, exceptions, _


class ResPartner(models.Model):
    _inherit = 'res.partner'

    website_id = fields.Char(string='Website')