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
    construction_contract_id = fields.Many2one(
        "construction.contract", string="Contrato de Obra", copy=False
    )
    commission_type = fields.Selection(
        related="construction_contract_id.commission_type",
        string="Tipo de Comisión",
        store=True,
        readonly=False,
    )

    def _create_invoices(self):
        invoice = super()._create_invoices()
        for order in self:
            contract = order.construction_contract_id
            if not contract:
                continue
            inv = invoice.filtered(lambda m: m.invoice_origin == order.name)
            if not inv:
                continue
            inv.invoice_line_ids = [(5, 0, 0)]
            # Buscar una cuenta de ingresos (primer ingreso disponible)
            account_income = self.env["account.account"].search(
                [("account_type", "=", "income"), ("company_id", "=", order.company_id.id)],
                limit=1,
            )
            lines = []
            if contract.commission_type == "full":
                lines.append(
                    (
                        0,
                        0,
                        {
                            "name": "Reembolso de costos proveedores",
                            "price_unit": contract.total_supplier_cost,
                            "quantity": 1,
                            "account_id": account_income.id,
                        },
                    )
                )
            lines.append(
                (
                    0,
                    0,
                    {
                        "name": f"Comisión de gestión {contract.commission_rate}%",
                        "price_unit": contract.commission_amount,
                        "quantity": 1,
                        "account_id": account_income.id,
                    },
                )
            )
            inv.write({
                "invoice_line_ids": lines,
                "construction_contract_id": contract.id,
            })
        return invoice
