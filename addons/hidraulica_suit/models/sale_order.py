from odoo import fields, models


class SaleOrder(models.Model):
    _inherit = "sale.order"

    code_inv = fields.Char(string="Código de la inversión")
    program_id = fields.Many2one("work.program", string="Programa")
    type_service = fields.Selection(
        [
            ("inversion", "Inversión"),
            ("mantenimiento", "Mantenimiento"),
            ("obra", "Preparación de Obra"),
        ],
        string="Tipo de Servicio",
    )
    inv_direct = fields.Many2one(
        "res.partner", string="Invercionista Directo (Contratista)"
    )
    benefited_pop = fields.Char(string="Población Beneficiada")
    is_existente_mep = fields.Boolean(string="Existencia de la ficha del MEP")
    is_prp = fields.Boolean(string="Tiene presupuesto aprobado")
    is_proyect = fields.Boolean(string="Tiene proyecto")
    is_microlocalization = fields.Boolean(string="Tiene Microlocalización")
    is_defense = fields.Boolean(string="Tiene compatibilización con la defensa")
    is_citma = fields.Boolean(string="Tiene dictamen del CITMA")
    is_licence = fields.Boolean(string="Tiene licencia de obra")
    is_timeline = fields.Boolean(string="Tiene Cronograma de ejecución de obra")
