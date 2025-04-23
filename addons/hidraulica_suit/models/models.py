# from odoo import models, fields, api


# class hidraulica_suit(models.Model):
#     _name = 'hidraulica_suit.hidraulica_suit'
#     _description = 'hidraulica_suit.hidraulica_suit'

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100
