# -*- coding: utf-8 -*-

from odoo import api, fields, models
from odoo.exceptions import UserError

class ProductCategory(models.Model):
    _inherit = "product.category"

    attribute_categ_ids = fields.Many2many('line.attribute.category', string="Attribute Categories")

class ProductTemplate(models.Model):
    _inherit = "product.template"

    attribute_categ_ids = fields.Many2many('line.attribute.category', string="Attribute Categories")
    attribute_theme_ids = fields.Many2many('line.attribute.theme', string="Attribute Themes")
