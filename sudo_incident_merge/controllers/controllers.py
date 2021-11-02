# -*- coding: utf-8 -*-
# from odoo import http


# class SupportHelpdeskSudoIncidentMerge(http.Controller):
#     @http.route('/sudo_incident_merge/sudo_incident_merge/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/sudo_incident_merge/sudo_incident_merge/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('sudo_incident_merge.listing', {
#             'root': '/sudo_incident_merge/sudo_incident_merge',
#             'objects': http.request.env['sudo_incident_merge.sudo_incident_merge'].search([]),
#         })

#     @http.route('/sudo_incident_merge/sudo_incident_merge/objects/<model("sudo_incident_merge.sudo_incident_merge"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('sudo_incident_merge.object', {
#             'object': obj
#         })
