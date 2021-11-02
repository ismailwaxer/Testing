# -*- coding: utf-8 -*-
# from odoo import http


# class SudoIncidentManagement(http.Controller):
#     @http.route('/sudo_incident_management/sudo_incident_management/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/sudo_incident_management/sudo_incident_management/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('sudo_incident_management.listing', {
#             'root': '/sudo_incident_management/sudo_incident_management',
#             'objects': http.request.env['sudo_incident_management.sudo_incident_management'].search([]),
#         })

#     @http.route('/sudo_incident_management/sudo_incident_management/objects/<model("sudo_incident_management.sudo_incident_management"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('sudo_incident_management.object', {
#             'object': obj
#         })
