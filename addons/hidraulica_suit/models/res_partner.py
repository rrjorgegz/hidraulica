from odoo import fields, models


class ResPartner(models.Model):
    _inherit = "res.partner"

    code = fields.Char()
    director_g = fields.Char(string="Director General")
    director_td = fields.Char(string="Director Desarrollo Tecnológico")
    director_hhrr = fields.Char(string="Director Capital Humano")
    director_a = fields.Char(string="Director Contabilidad y finanza")
    especialista = fields.Char(string="Especialista Principal de Grupo")
