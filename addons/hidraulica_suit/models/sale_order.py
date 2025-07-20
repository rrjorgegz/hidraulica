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
    commission_type = fields.Selection(
        [
            ('full', 'Factura Completa (Costos + Comisión)'),
            ('commission_only', 'Solo Comisión')
        ],
        string='Tipo de Comisión',
        default='full'
    )

    def _create_invoices(self):  
        invoice = super()._create_invoices()  
        # Calcular costo total de proveedores (desde facturas vinculadas al centro analítico)  
        total_cost = self.analytic_account_id.total_cost  
        commission = total_cost * 0.05  # 5%  
        # Borrar líneas de factura estándar (generadas desde SO)  
        invoice.invoice_line_ids = False  
        # Añadir línea de comisión  
        invoice.write({  
            'invoice_line_ids': [(0, 0, {  
                'name': 'Comisión de Gestión (5%)',  
                'price_unit': commission,  
                'account_id': ... # Cuenta contable para comisiones  
            })]  
        })  
        # Si es "full", añadir línea con costos de proveedores  
        if self.commission_type == 'full':  
            invoice.write({  
                'invoice_line_ids': [(0, 0, {  
                    'name': 'Costos de Proveedores',  
                    'price_unit': total_cost,  
                    'account_id': ... # Cuenta contable para costos  
                })]  
            })  
        return invoice 
