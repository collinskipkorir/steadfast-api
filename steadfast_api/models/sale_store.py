# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

import requests
from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError
from odoo.addons.payment import utils as payment_utils

class SaleStore(models.Model):
    _name = "sale.store"
    _check_company_auto = True
    
    name = fields.Char(string="Name")