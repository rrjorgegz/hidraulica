from odoo import fields, models


class AccountMove(models.Model):
    _inherit = "account.move"

    construction_contract_id = fields.Many2one(
        "construction.contract", string="Contrato de Obra", copy=False
    )
