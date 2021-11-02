import json
import logging
import re

from odoo import api, fields, models, tools, _
from odoo.exceptions import UserError, ValidationError
from odoo.osv import expression

from odoo.tools import float_compare

_logger = logging.getLogger(__name__)


class SudoCategory(models.Model):
    _name = 'sudo_incident.category'
    _description = 'Incident Category'

    _rec_name = 'complete_name'
    _order = 'complete_name'

    _parent_store = True
    _parent_name = "parent_id"

    name = fields.Char('Category', index=True, required=True)
    complete_name = fields.Char(
        'Complete Name',compute='_compute_complete_name',
        store=True)

    parent_id = fields.Many2one(
        'sudo_incident.category',
        string='Parent Category',
        ondelete='restrict',
        index=True
    )

    child_ids = fields.One2many(
        'sudo_incident.category', 'parent_id',
        string='Child Categories')

    parent_path = fields.Char(index=True)
    parent_id_domain = fields.Char(compute="_compute_parent_id_domain", readonly=True, store=False, )

    @api.depends('parent_id')
    def _compute_parent_id_domain(self):

        for rec in self:
            rec.parent_id_domain = json.dumps(
                [('parent_id', '=', rec.parent_id.id)]
            )

    @api.depends('name', 'parent_id.complete_name')
    def _compute_complete_name(self):
        for rec in self:
            if rec.parent_id:
                rec.complete_name = '%s / %s' % (rec.parent_id.complete_name, rec.name)
            else:
                rec.complete_name = rec.name

    @api.constrains('parent_id')
    def _check_hierarchy(self):
        if not self._check_recursion():
            raise models.ValidationError('Error! You cannot create recursive categories.')


