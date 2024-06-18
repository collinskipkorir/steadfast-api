# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

import requests
from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError
from odoo.addons.payment import utils as payment_utils

class SteadfastOrder(models.Model):
    _name = "steadfast.order"
    _check_company_auto = True
    
    consignment_id = fields.Char(string="Consignment Id", readonly=True)
    invoice = fields.Char(string="Invoice", readonly=True)
    tracking_code = fields.Char(string="Tracking Code", readonly=True)
    recipient_name = fields.Char(string="Recipient Name", readonly=True)
    recipient_phone = fields.Char(string="Recipient Phone", readonly=True)
    recipient_address = fields.Char(string="Recipient Address", readonly=True)
    cod_amount = fields.Char(string="Cod Amount", readonly=True)
    status = fields.Char(string="Status", readonly=True)
    note = fields.Char(string="Note", readonly=True)
    created_at = fields.Datetime(string="Created At", readonly=True)
    updated_at = fields.Datetime(string="Updated At", readonly=True)
    delivery_status = fields.Char(string="Delivery Status", readonly=True)
    company_id = fields.Many2one('res.company', 'Company', required=True, index=True)
    
    def check_status(self):
        for order in self:
               cid = order.consignment_id
               invoice = order.invoice
               tracking_code = order.tracking_code
               steadfast_credentials = self.env["steadfast.credential"].sudo().search([])
               for credential in steadfast_credentials:
                    api_url = credential.api_url
                    api_key = credential.api_key
                    secret_key = credential.secret_key
               try:
                   if cid:
                        status_api = f"{api_url}/status_by_cid/{cid}"
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
                            delivery_status = data.get("delivery_status")
                            order.delivery_status = delivery_status
                        else:
                            print(f"Failed to send data to /steadfast route. Status code: {response.status_code}")
               except Exception as e:
                    print(f"An error occurred: {e}")
                    