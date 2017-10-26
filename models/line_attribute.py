# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from odoo.addons import decimal_precision as dp
from odoo.exceptions import UserError

class LineAttributeCategory(models.Model):
    _name = "line.attribute.category"
    _description = 'Sale Line Attribute Category'

    name = fields.Char("Category name", required=True)

class LineAttributeLine(models.Model):
    _name = "line.attribute.line"
    _description = 'Sale Line Attribute Line'

    attribute_id = fields.Many2one('line.attribute', string="Attribute", required=True)
    categ_id = fields.Many2one('line.attribute.category', string="Attribute", required=True)
    value = fields.Char("Attribute Value", ondelete='set null')

class LineAttribute(models.Model):
    _name = "line.attribute"
    _description = 'Sale Line Attributes'

    order_line = fields.Many2one('sale.order.line', string="Sale Order Line")
    attribute_values = fields.One2many('line.attribute.line', 'attribute_id', 'Attribute Values')
