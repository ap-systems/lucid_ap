# -*- coding: utf-8 -*-
# from odoo import http


# class LucidTimesheet(http.Controller):
#     @http.route('/lucid_timesheet/lucid_timesheet', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/lucid_timesheet/lucid_timesheet/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('lucid_timesheet.listing', {
#             'root': '/lucid_timesheet/lucid_timesheet',
#             'objects': http.request.env['lucid_timesheet.lucid_timesheet'].search([]),
#         })

#     @http.route('/lucid_timesheet/lucid_timesheet/objects/<model("lucid_timesheet.lucid_timesheet"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('lucid_timesheet.object', {
#             'object': obj
#         })
