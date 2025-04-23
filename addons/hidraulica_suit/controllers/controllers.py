# from odoo import http


# class HidraulicaSuit(http.Controller):
#     @http.route('/hidraulica_suit/hidraulica_suit', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/hidraulica_suit/hidraulica_suit/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('hidraulica_suit.listing', {
#             'root': '/hidraulica_suit/hidraulica_suit',
#             'objects': http.request.env['hidraulica_suit.hidraulica_suit'].search([]),
#         })
