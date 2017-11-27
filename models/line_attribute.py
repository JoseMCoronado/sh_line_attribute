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

    @api.multi
    @api.constrains('categ_id','value')
    def rename_description(self):
        for line in self:
            parsed_desc = line.attribute_id.order_line.name.split("---")
            second_package = "---" + '\n'
            for values in line.attribute_id.attribute_values:
                second_package += str(values.categ_id.name) + ': ' + str(values.value) + '\n'
                print str(values.categ_id.name) + ': ' + str(values.value) + '\n'
            new_desc = str(parsed_desc[0]) + second_package
            line.attribute_id.order_line.write({'name':new_desc})
            for inv_line in line.attribute_id.order_line.invoice_lines:
                inv_line.write({'name':new_desc})

class LineAttribute(models.Model):
    _name = "line.attribute"
    _description = 'Sale Line Attributes'

    order_line = fields.Many2one('sale.order.line', string="Sale Order Line")
    attribute_values = fields.One2many('line.attribute.line', 'attribute_id', 'Attribute Values')
