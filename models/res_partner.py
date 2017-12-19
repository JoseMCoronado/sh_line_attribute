# -*- coding: utf-8 -*-

from odoo import api, fields, models
from odoo.exceptions import UserError

class ResPartner(models.Model):
    _inherit = 'res.partner'

    attribute_theme_ids = fields.Many2many('line.attribute.theme', string="Attribute Themes")
