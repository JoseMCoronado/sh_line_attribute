# -*- coding: utf-8 -*-

from odoo import api, fields, models
from odoo.exceptions import UserError

class ProductCategory(models.Model):
    _inherit = "product.category"

    attribute_categ_ids = fields.Many2many('line.attribute.category', string="Attribute Categories", required=True)
