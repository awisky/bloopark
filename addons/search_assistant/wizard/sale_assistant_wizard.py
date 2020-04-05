# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

import uuid

from itertools import groupby
from datetime import datetime, timedelta
from werkzeug.urls import url_encode

from odoo import api, fields, models, _
from odoo.exceptions import UserError, AccessError
from odoo.osv import expression
from odoo.tools import float_is_zero, float_compare, DEFAULT_SERVER_DATETIME_FORMAT

from odoo.tools.misc import formatLang

from odoo.addons import decimal_precision as dp
from ast import literal_eval
import logging

_logger = logging.getLogger(__name__)


class SearchAssistantLine(models.TransientModel):
    """
    """
    _inherit = "search.assistant.line"


class SearchAssistant(models.TransientModel):
    """
    """
    _inherit = "search.assistant"
    _description = "Search Assistant"

    @api.model
    def _default_partner_id(self):
        """
        """
        value=super(SearchAssistant,self)._default_partner_id()
        if self._context.get('create',False)=='sale.order':
            sale_default_partner_id = self.env['ir.config_parameter'].sudo().get_param(
                'search_assistant.sale_default_partner_id', default='False')
            value = literal_eval(sale_default_partner_id)
        return value

    partner_id = fields.Many2one(
        'res.partner', string='Partner', default=_default_partner_id, required=True)

    def action_view_sale_order(self, sale_order_id):

        action = self.env.ref('sale.action_orders').read()[0]

        form_view = [(self.env.ref('sale.view_order_form').id, 'form')]
        action['views'] = form_view
        action['res_id'] = sale_order_id
        _logger.debug(action)
        return action

    def create_sale_order(self):
        """

        """
        line_obj = self.env['sale.order.line']
        sale_obj = self.env['sale.order']
        lines = []
        must = False

        if self.partner_id:
            for search_wizard in self:
                selection = [
                    line for line in search_wizard.line_ids if line.selected]
                if len(selection) > 0:
                    vals = {
                        'partner_id': self.partner_id.id
                    }
                    sale_order = sale_obj.create(vals)
                    for line in search_wizard.line_ids:
                        if line.selected:
                            values = {
                                'name': 'something',
                                'order_id': sale_order.id,
                                'product_id': line.product_id.id,
                            }

                            values.update(
                                line_obj._prepare_add_missing_fields(values))
                            values.update(
                                {'product_uom_qty': line.product_uom_qty})

                            line_obj.create(values)
                    return self.action_view_sale_order(sale_order.id)
