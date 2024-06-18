# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

import requests
from odoo import api, fields, models, SUPERUSER_ID, _
from odoo.exceptions import UserError, ValidationError
from odoo.addons.payment import utils as payment_utils

class SteadfastCredential(models.Model):
    _name = "steadfast.credential"
    _check_company_auto = True
    
    api_url = fields.Char(string="Base Url")
    api_key = fields.Char(string="API Key")
    secret_key = fields.Char(string="Secret Key")
    balance = fields.Char("Balance", readonly=True)
    company_id = fields.Many2one('res.company', 'Company', required=True, index=True, default=lambda self: self.env.company)
    store_id = fields.Many2one('sale.store', string="Store")

    
    def check_balance(self):
        print(f"Company ----------------> {self.company_id.name}")
        steadfast_credentials = self.env["steadfast.credential"].sudo().search([])
        for credential in steadfast_credentials:
            api_url = credential.api_url
            api_key = credential.api_key
            secret_key = credential.secret_key
            status_api = f"{api_url}/get_balance"
            response = requests.get(status_api,
                headers={
                    'Content-Type': 'application/json',
                    'Api-Key': api_key,
                    'Secret-Key': secret_key
                })
            # Check if the request was successful
            response.raise_for_status()
            data = response.json()
            print(f"response ---------------------------> {data}")
            if data.get('status') == 400:
                error_message = "Error(s) encountered:\n"
                for field, errors in data['errors'].items():
                    error_message += f"- {field}: {', '.join(errors)}\n"
                # Raise UserError to display the error message as a warning popup
                raise ValidationError(error_message)
            
            if response.status_code == 200:
                print(f"Current Balance ---------------> {data.get('current_balance')}")
                credential.balance = data.get('current_balance')
            else:
                print(f"Failed to send data to /steadfast route. Status code: {response.status_code}")
    
    