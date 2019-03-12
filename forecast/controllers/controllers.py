# -*- coding: utf-8 -*-
from odoo import http

# class Forecast(http.Controller):
#     @http.route('/forecast/forecast/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/forecast/forecast/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('forecast.listing', {
#             'root': '/forecast/forecast',
#             'objects': http.request.env['forecast.forecast'].search([]),
#         })

#     @http.route('/forecast/forecast/objects/<model("forecast.forecast"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('forecast.object', {
#             'object': obj
#         })