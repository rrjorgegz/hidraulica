from odoo import fields, models


class WorkProgram(models.Model):
    _name = "work.program"
    _description = "Programa"

    name = fields.Char(string="Nombre")
