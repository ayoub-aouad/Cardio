# -*- coding: utf-8 -*-
# from odoo import http


# class Hospitalisation(http.Controller):
#     @http.route('/hospitalisation/hospitalisation', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/hospitalisation/hospitalisation/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('hospitalisation.listing', {
#             'root': '/hospitalisation/hospitalisation',
#             'objects': http.request.env['hospitalisation.hospitalisation'].search([]),
#         })

#     @http.route('/hospitalisation/hospitalisation/objects/<model("hospitalisation.hospitalisation"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('hospitalisation.object', {
#             'object': obj
#         })
