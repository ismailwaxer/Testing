# -*- coding: utf-8 -*-
# from odoo import http


# class SudoIncident(http.Controller):
#     @http.route('/sudo_incident/sudo_incident/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/sudo_incident/sudo_incident/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('sudo_incident.listing', {
#             'root': '/sudo_incident/sudo_incident',
#             'objects': http.request.env['sudo_incident.sudo_incident'].search([]),
#         })

#     @http.route('/sudo_incident/sudo_incident/objects/<model("sudo_incident.sudo_incident"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('sudo_incident.object', {
#             'object': obj
#         })
