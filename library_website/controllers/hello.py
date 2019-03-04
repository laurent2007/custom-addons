from odoo import http

class Hello(http.Controller):
    @http.route('/helloworld',auth="public")
    def helloworld(self):
        return('<h1> Hello World !</h1>')
