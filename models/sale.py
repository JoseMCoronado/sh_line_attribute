# -*- coding: utf-8 -*-

from odoo import api, fields, models
from odoo.exceptions import UserError

class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    attribute_id = fields.Many2one('line.attribute', 'Custom Attributes',copy=False, index=True)

    @api.multi
    def open_attribute_values(self):
        self.ensure_one()
        for line in self:
            if not line.attribute_id:
                new_attribute = line.env['line.attribute'].create({'order_line':line.id})
                line.attribute_id = new_attribute
                attribute_categories = line.product_id.product_tmpl_id.categ_id.attribute_categ_ids
                if attribute_categories:
                    for categ in attribute_categories:
                        new_line = line.env['line.attribute.line'].create({
                        'categ_id':categ.id,
                        'attribute_id':new_attribute.id,
                        })
                #attribute_view = new_attribute.id
                action_data = line.env.ref('sh_line_attribute.action_window_line_attribute').read()[0]
                action_data.update({'res_id':line.attribute_id.id})
                return action_data
            else:
                action_data = line.env.ref('sh_line_attribute.action_window_line_attribute').read()[0]
                #attribute_form_id = line.env['line.attribute'].search([()'order_line','=',line.id)],limit=1).id
                action_data.update({'res_id':line.attribute_id.id})
                return action_data
