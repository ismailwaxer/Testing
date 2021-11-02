# -*- coding: utf-8 -*-
# from odoo import http


# class SudoHelpdeskDate(http.Controller):
#     @http.route('/sudo_helpdesk_date/sudo_helpdesk_date/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/sudo_helpdesk_date/sudo_helpdesk_date/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('sudo_helpdesk_date.listing', {
#             'root': '/sudo_helpdesk_date/sudo_helpdesk_date',
#             'objects': http.request.env['sudo_helpdesk_date.sudo_helpdesk_date'].search([]),
#         })

#     @http.route('/sudo_helpdesk_date/sudo_helpdesk_date/objects/<model("sudo_helpdesk_date.sudo_helpdesk_date"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('sudo_helpdesk_date.object', {
#             'object': obj
#         })
