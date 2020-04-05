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
    _name = "search.assistant.line"
    _description = "Search Assistant Line"

    search_id = fields.Many2one('search.assistant', string='Search')
    selected = fields.Boolean('')
    description = fields.Char('Description')
    attribute_value_ids = fields.Many2many(
        'product.template.attribute.value', string="Attribute Values")
    product_id = fields.Many2one('product.product', string='Product')
    product_uom_qty = fields.Float(string='Quantity', digits='Product Unit of Measure', required=True, default=1.0)

    @api.onchange('selected')
    def on_change_selected(self):
        _logger.debug('====> on_change_selected line====>')


class SearchAssistant(models.TransientModel):
    """
    """
    _name = "search.assistant"
    _description = "Search Assistant"

    @api.model
    def _default_partner_id(self):
        """
        """
        return False

    partner_id = fields.Many2one(
        'res.partner', string='Partner', default=_default_partner_id, required=True)

    attribute_ids = fields.Many2many(
        'product.attribute', string='Product Attribute')
    attribute_value_ids = fields.Many2many(
        'product.template.attribute.value', string="Attribute Values")
    description = fields.Char(string='Description')
    line_ids = fields.One2many(
        'search.assistant.line', 'search_id', string='Search Results')
    selected = fields.Boolean('')

    def make_domain(self, domain_name, code):
        """
        This stuff is done to allow flexibility search
        """
        domain_code = " and "+domain_name + " ilike  %s "
        if code:
            i = code.find(' ')
            domain_code = ""
            while i != -1:
                domain_code += " and "+domain_name + " ilike  %s "
                code = code[i+1:]
                i = code.find(' ')
            domain_code += " and "+domain_name + " ilike  %s "
        _logger.debug('====> domain_code ====> %s' % domain_code)
        return domain_code

    def insert_domain(self, domain_name, code):
        """
        Dinamicaly creates the domain insertion parameters for the domain created before!
        """
        domain_code = (code)
        if code:
            i = code.find(' ')
            domain_code = ()
            while i != -1:
                domain_code += ('%'+code[:i]+'%',)
                code = code[i+1:]
                i = code.find(' ')
            domain_code += ('%'+code+'%',)
        _logger.debug(domain_code)
        return domain_code

    @api.onchange('selected')
    def on_change_selected(self):
        """
        """
        _logger.debug('====> on_change_selected main====>')

    @api.onchange('attribute_value_ids')
    def search(self):
        """
        """
        _logger.debug('====> filter activated ====>')
        product_obj = self.env['product.product']
        
        domain = []
        filter_values = []


        filter_values=list(set(self.attribute_value_ids.ids))
        
        domain = [('product_template_attribute_value_ids', 'in', filter_values)]
        _logger.debug('====> domain ====> %s' % domain)
        product_ids = product_obj.search(domain)
        line_ids = []
        search_line_obj = self.env['search.assistant.line']
        for product in product_ids:
            line_ids.append((0,0,{ 
                'selected': True,
                'product_id': product.id,
                'attribute_value_ids': False,
                'attribute_value_ids': [(6, 0, product.product_template_attribute_value_ids.ids)],
                'description': product.description or '',
            }))
        self.line_ids = line_ids

    
                    
    
    
    
       
