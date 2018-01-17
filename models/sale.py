# -*- coding: utf-8 -*-

from odoo import api, fields, models
from odoo.exceptions import UserError

class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    attribute_id = fields.Many2one('line.attribute', 'Custom Attributes',copy=False, index=True)
    show_full_circle = fields.Boolean(string='Show Full (Technical)',compute='_show_full_circle', readonly=True,store=False)

    @api.constrains('product_id')
    def create_attribute_id(self):
        for line in self:
            if line.attribute_id:
                line.attribute_id.unlink()
            new_attribute = line.env['line.attribute'].create({'order_line':line.id})
            line.attribute_id = new_attribute
            attribute_categories = None
            if line.product_id.product_tmpl_id.attribute_theme_ids and len(line.product_id.product_tmpl_id.attribute_theme_ids) == 1:
                if line.product_id.product_tmpl_id.attribute_theme_ids[0].attribute_values:
                    for theme_line in line.product_id.product_tmpl_id.attribute_theme_ids[0].attribute_values:
                        new_line = line.env['line.attribute.line'].create({
                        'categ_id':theme_line.categ_id.id,
                        'value':theme_line.value,
                        'attribute_id':new_attribute.id,
                        })
            elif line.product_id.product_tmpl_id.categ_id.attribute_categ_ids:
                attribute_categories = line.product_id.product_tmpl_id.categ_id.attribute_categ_ids
            if attribute_categories:
                for categ in attribute_categories:
                    new_line = line.env['line.attribute.line'].create({
                    'categ_id':categ.id,
                    'attribute_id':new_attribute.id,
                    })

    @api.multi
    def open_attribute_values(self):
        self.ensure_one()
        for line in self:
            if not line.attribute_id:
                new_attribute = line.env['line.attribute'].create({'order_line':line.id})
                line.attribute_id = new_attribute
                attribute_categories = None
                if line.product_id.product_tmpl_id.attribute_categ_ids:
                    attribute_categories = line.product_id.product_tmpl_id.attribute_categ_ids
                elif line.product_id.product_tmpl_id.categ_id.attribute_categ_ids:
                    attribute_categories = line.product_id.product_tmpl_id.categ_id.attribute_categ_ids
                if attribute_categories:
                    for categ in attribute_categories:
                        new_line = line.env['line.attribute.line'].create({
                        'categ_id':categ.id,
                        'attribute_id':new_attribute.id,
                        })
                action_data = line.env.ref('sh_line_attribute.action_window_line_attribute').read()[0]
                action_data.update({'res_id':line.attribute_id.id})
                line.attribute_id.render_domain = False
                return action_data
            else:
                action_data = line.env.ref('sh_line_attribute.action_window_line_attribute').read()[0]
                action_data.update({'res_id':line.attribute_id.id})
                line.attribute_id.render_domain = False
                return action_data

    @api.multi
    def _show_full_circle(self):
        for line in self:
            line.show_full_circle = False
            if any(l.value != False for l in line.attribute_id.attribute_values):
                line.show_full_circle = True
