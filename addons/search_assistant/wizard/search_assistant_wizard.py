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

    product_uom_qty = fields.Float(
        string='Quantity', digits='Product Unit of Measure', required=True, default=1.0)




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
    category_ids = fields.Many2many(
        'product.category', string="Product Category")
    code = fields.Char(string='Code')

    description = fields.Char(string='Description',
                              help='Enter the description spaces split your query in \
                                    case you forgot how was your product description.')
    line_ids = fields.One2many(
        'search.assistant.line', 'search_id', string='Search Results')
    selected = fields.Boolean('')

    def make_domain(self, domain_name, code):
        """
        This function builds a domain spliting the code by spaces
        """
        domain_code= [(domain_name,'ilike','%')]
        if code:
            i=code.find(' ')
            domain_code=[]
            while i!= -1:
                domain_code.append((domain_name,'ilike',code[0:i]))
                code=code[i+1:]
                i=code.find(' ')
            domain_code.append((domain_name,'ilike',code))
        return domain_code



    @api.onchange('attribute_ids','attribute_value_ids','description','selected','category_ids','code')
    def search(self):
        """
        """
        _logger.debug('====> filter activated ====>')
        product_obj = self.env['product.product']
        product_attribute_obj = self.env['product.template.attribute.value']
        domain = []
        
        attribute_ids = list(set(self.attribute_ids.ids))
        attribute_values_ids = list(set(self.attribute_value_ids.ids))
        category_ids = list(set(self.category_ids.ids))
        description = self.description
        code = self.code

        if description and len(description)>0:
            for description_domain in self.make_domain('name',description):
                domain.append(description_domain)
        if code and len(code)>0:
            for code_domain in self.make_domain('default_code',code):
                domain.append(code_domain)
        
        if len(attribute_values_ids)>0:
            domain.append(('product_template_attribute_value_ids', 'in', attribute_values_ids))
        else:
            if len(attribute_ids)>0:
                attribute_ids=product_attribute_obj.search([('attribute_id','in',attribute_ids)]).ids
                domain.append(('product_template_attribute_value_ids', 'in', attribute_ids))
        
        if len(category_ids)>0:
            domain.append(('categ_id', 'in', category_ids))
        _logger.debug('====> domain ====> %s' % domain)
        self.line_ids = False
        
        if len(domain)>0:
            product_ids = product_obj.search(domain)
            line_ids = []
            search_line_obj = self.env['search.assistant.line']
            
            for product in product_ids:
                line_ids.append((0, 0, {
                    'selected': self.selected,
                    'product_id': product.id,
                    'attribute_value_ids': False,
                    'attribute_value_ids': [(6, 0, product.product_template_attribute_value_ids.ids)],
                    'description': product.description or '',
                }))
            self.line_ids = line_ids
