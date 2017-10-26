# -*- coding: utf-8 -*-

from odoo import api, fields, models
from odoo.exceptions import UserError

class AccountInvoiceLine(models.Model):
    _inherit = "account.invoice.line"

    attribute_id = fields.Many2one('line.attribute','Custom Attributes', compute='_compute_attribute', store=False)

    @api.depends('sale_line_ids','sale_line_ids.attribute_id')
    def _compute_attribute(self):
        for line in self:
            if line.sale_line_ids and line.sale_line_ids[0].attribute_id:
                line.attribute_id = line.sale_line_ids[0].attribute_id

    @api.multi
    def open_attribute_values(self):
        self.ensure_one()
        for line in self:
                action_data = line.env.ref('sh_line_attribute.action_window_line_attribute').read()[0]
                action_data.update({'res_id':line.attribute_id.id})
                return action_data
