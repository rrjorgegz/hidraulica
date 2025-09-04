from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class ConstructionContract(models.Model):
    _name = "construction.contract"
    _description = "Solicitud / Contrato de Obra"
    _inherit = ["mail.thread", "mail.activity.mixin"]

    name = fields.Char(string="Referencia", required=True, copy=False, default="Nuevo")
    partner_id = fields.Many2one("res.partner", string="Cliente", required=True, tracking=True)
    project_name = fields.Char(string="Nombre de la Obra", required=True, tracking=True)
    sale_id = fields.Many2one("sale.order", string="Orden de Venta", copy=False)
    analytic_account_id = fields.Many2one(
        "account.analytic.account", string="Cuenta Analítica", tracking=True
    )
    program_id = fields.Many2one("work.program", string="Programa")
    estimated_cost = fields.Monetary(string="Costo Estimado Proveedores")
    commission_rate = fields.Float(
        string="% Comisión", default=5.0, help="Porcentaje de comisión sobre los costos aceptados"
    )
    commission_type = fields.Selection(
        [
            ("full", "Factura Completa (Costos + Comisión)"),
            ("commission_only", "Solo Comisión"),
        ],
        default="full",
        required=True,
        tracking=True,
    )
    currency_id = fields.Many2one(
        "res.currency", default=lambda self: self.env.company.currency_id.id, required=True
    )
    state = fields.Selection(
        [
            ("draft", "Borrador"),
            ("confirmed", "Confirmado"),
            ("in_progress", "En Progreso"),
            ("done", "Terminado"),
            ("cancel", "Cancelado"),
        ],
        default="draft",
        tracking=True,
    )

    supplier_cost_ids = fields.One2many(
        "construction.contract.cost", "contract_id", string="Costos Proveedores"
    )
    total_supplier_cost = fields.Monetary(
        string="Costo Total Proveedores", compute="_compute_totals", store=True
    )
    commission_amount = fields.Monetary(
        string="Comisión", compute="_compute_totals", store=True
    )
    amount_to_invoice = fields.Monetary(
        string="Monto a Facturar", compute="_compute_totals", store=True
    )

    @api.depends("supplier_cost_ids.subtotal", "commission_rate", "commission_type")
    def _compute_totals(self):
        for rec in self:
            total_cost = sum(rec.supplier_cost_ids.mapped("subtotal"))
            rec.total_supplier_cost = total_cost
            commission = total_cost * (rec.commission_rate / 100.0)
            rec.commission_amount = commission
            if rec.commission_type == "full":
                rec.amount_to_invoice = total_cost + commission
            else:
                rec.amount_to_invoice = commission

    @api.constrains("commission_rate")
    def _check_commission_rate(self):
        for rec in self:
            if rec.commission_rate < 0 or rec.commission_rate > 5:
                raise ValidationError(_("La comisión no puede exceder el 5%"))

    def action_confirm(self):
        for rec in self:
            if rec.state != "draft":
                continue
            if not rec.sale_id:
                rec._create_sale_order()
            rec.state = "confirmed"
        return True

    def action_progress(self):
        self.filtered(lambda r: r.state == "confirmed").write({"state": "in_progress"})

    def action_done(self):
        self.filtered(lambda r: r.state in ("in_progress", "confirmed")).write({"state": "done"})

    def action_cancel(self):
        self.write({"state": "cancel"})

    def _create_sale_order(self):
        self.ensure_one()
        so_vals = {
            "partner_id": self.partner_id.id,
            "construction_contract_id": self.id,
            "type_service": "obra",
            "program_id": self.program_id.id,
        }
        sale = self.env["sale.order"].create(so_vals)
        self.sale_id = sale.id
        return sale

    def action_create_invoice(self):
        self.ensure_one()
        if not self.sale_id:
            self._create_sale_order()
        # Generar factura manual con líneas según commission_type
        move = self.env["account.move"].create(
            {
                "move_type": "out_invoice",
                "partner_id": self.partner_id.id,
                "invoice_origin": self.name,
                "construction_contract_id": self.id,
                "currency_id": self.currency_id.id,
                "invoice_line_ids": [(5, 0, 0)],
            }
        )
        account_income = self.env.company.get_chart_template_id().property_account_income_categ_id
        # fallback: buscar primera cuenta de ingresos
        if not account_income:
            account_income = self.env["account.account"].search(
                [("user_type_id.type", "=", "income"), ("company_id", "=", self.env.company.id)], limit=1
            )
        lines = []
        if self.commission_type == "full":
            # Resumen de costos
            lines.append(
                (
                    0,
                    0,
                    {
                        "name": "Reembolso de costos proveedores",
                        "quantity": 1,
                        "price_unit": self.total_supplier_cost,
                        "account_id": account_income.id,
                    },
                )
            )
        # Comisión
        lines.append(
            (
                0,
                0,
                {
                    "name": f"Comisión de gestión {self.commission_rate}%",
                    "quantity": 1,
                    "price_unit": self.commission_amount,
                    "account_id": account_income.id,
                },
            )
        )
        move.write({"invoice_line_ids": lines})
        return {
            "type": "ir.actions.act_window",
            "res_model": "account.move",
            "res_id": move.id,
            "view_mode": "form",
        }


class ConstructionContractCost(models.Model):
    _name = "construction.contract.cost"
    _description = "Costo Proveedor Obra"

    contract_id = fields.Many2one(
        "construction.contract", string="Contrato", required=True, ondelete="cascade"
    )
    supplier_id = fields.Many2one(
        "res.partner", string="Proveedor", domain=[("supplier_rank", ">", 0)], required=True
    )
    description = fields.Char(string="Descripción")
    quantity = fields.Float(default=1.0)
    price_unit = fields.Monetary(string="Precio Unitario", required=True)
    subtotal = fields.Monetary(
        string="Subtotal", compute="_compute_subtotal", store=True
    )
    currency_id = fields.Many2one(
        related="contract_id.currency_id", store=True, readonly=True
    )

    @api.depends("quantity", "price_unit")
    def _compute_subtotal(self):
        for line in self:
            line.subtotal = line.quantity * line.price_unit
