# -*- coding: utf-8 -*-
# from odoo import http


# class SudoAceCrm(http.Controller):
#     @http.route('/sudo_ace_crm/sudo_ace_crm/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/sudo_ace_crm/sudo_ace_crm/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('sudo_ace_crm.listing', {
#             'root': '/sudo_ace_crm/sudo_ace_crm',
#             'objects': http.request.env['sudo_ace_crm.sudo_ace_crm'].search([]),
#         })

#     @http.route('/sudo_ace_crm/sudo_ace_crm/objects/<model("sudo_ace_crm.sudo_ace_crm"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('sudo_ace_crm.object', {
#             'object': obj
#         })
