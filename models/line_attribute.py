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

    attribute_id = fields.Many2one('line.attribute', string="Attribute")
    categ_id = fields.Many2one('line.attribute.category', string="Attribute")
    value = fields.Char("Attribute Value", ondelete='set null')

    @api.multi
    @api.constrains('categ_id','value')
    def rename_description(self):
        for line in self:
                parsed_desc = line.attribute_id.order_line.name.split("---")
                second_package = "---" + '\n'
                for values in line.attribute_id.attribute_values:
                    second_package += '    ' + str(values.categ_id.name) + ': ' + str(values.value) + '\n'
                new_desc = str(parsed_desc[0]) + second_package
                line.attribute_id.order_line.write({'name':new_desc})
                for inv_line in line.attribute_id.order_line.invoice_lines:
                    inv_line.write({'name':new_desc})

class LineAttribute(models.Model):
    _name = "line.attribute"
    _description = 'Sale Line Attributes'

    order_line = fields.Many2one('sale.order.line', string="Sale Order Line")
    attribute_values = fields.One2many('line.attribute.line', 'attribute_id', 'Attribute Values')
    theme_id = fields.Many2one('line.attribute.theme', string="Theme")
    attribute_theme_ids = fields.Many2many('line.attribute.theme', related="order_line.product_id.product_tmpl_id.attribute_theme_ids")

    @api.constrains('theme_id')
    def create_theme_lines(self):
        for session in self:
            if session.theme_id and session.theme_id != False:
                for line in session.attribute_values:
                    line.unlink()
                if session.theme_id.attribute_values:
                    for theme_line in session.theme_id.attribute_values:
                        new_line = session.env['line.attribute.line'].create({
                        'categ_id':theme_line.categ_id.id,
                        'value':theme_line.value,
                        'attribute_id':session.id,
                        })


class LineAttributeThemeLine(models.Model):

    _name = "line.attribute.theme.line"
    _description = 'Sale Line Attribute Theme Line'
    attribute_id = fields.Many2one('line.attribute.theme', string="Attribute")
    categ_id = fields.Many2one('line.attribute.category', string="Attribute")
    value = fields.Char("Attribute Value")

class LineAttributeTheme(models.Model):
    _name = "line.attribute.theme"
    _description = 'Sale Line Attributes Theme'

    name = fields.Char(string="Theme Name")
    attribute_values = fields.One2many('line.attribute.theme.line', 'attribute_id', 'Attribute Values')
