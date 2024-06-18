# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
import requests, json, logging
from datetime import datetime
from odoo.exceptions import ValidationError


class SaleOrder(models.Model):
     _inherit = "sale.order"

     custom_amount = fields.Float(
          string="Streadfast Amount",
          store=True,
          compute="compute_custom_amount",
          readonly=False,
     )
     store_id = fields.Many2one('sale.store', string="Store")

     @api.depends("amount_total")
     def compute_custom_amount(self):
          for order in self:
               if order.amount_total:
                    order.custom_amount = order.amount_total
               else:
                    order.custom_amount = 0.0

    #     def action_bulk_upload_button(self):
    #          data = []
    #          for order in self:
    #                order_data = {
    #                     'invoice' : order.name,
    #                     'recipient_name' : order.partner_id.name,
    #                     'recipient_phone' : order.partner_id.phone,
    #                     'recipient_address' : order.partner_id.contact_address,
    #                     'cod_amount' : order.amount_total
    #                }
    #                data.append(order_data)

    #          # Make an HTTP POST request to the API route
    #          logging.info(f"data ---------------------> {data}")
    #          json_data = json.dumps(data)
    #          steadfast_credentials = self.env["steadfast.credential"].sudo().search([])
    #          for credential in steadfast_credentials:
    #                api_url = credential.api_url
    #                api_key = credential.api_key
    #                secret_key = credential.secret_key

    #          response = requests.post(api_url+"/create_order/bulk-order", data=json_data,
    #                headers={
    #                     'Content-Type': 'application/json',
    #                     'Api-Key': api_key,
    #                     'Secret-Key': secret_key
    #                })

    #          # Check if the request was successful
    #          response.raise_for_status()
    #          data = response.json()
    #          logging.info(f"response ---------------------------> {data}")
    #          if response.status_code == 200:
    #                # Extract relevant information from the response to create the steadfast order record
    #                consignment_info = data.get("data")
    #                # Create records in the steadfast.order model
    #                for steadfast_orders in consignment_info:
    #                     steadfast_order = self.env['steadfast.order'].create({
    #                          'consignment_id': steadfast_orders.get('consignment_id'),
    #                          'invoice': steadfast_orders.get('invoice'),
    #                          'tracking_code': steadfast_orders.get('tracking_code'),
    #                          'recipient_name': steadfast_orders.get('recipient_name'),
    #                          'recipient_phone': steadfast_orders.get('recipient_phone'),
    #                          'recipient_address': steadfast_orders.get('recipient_address'),
    #                          'cod_amount': steadfast_orders.get('cod_amount'),
    #                          'status': steadfast_orders.get('status'),
    #                          'note': steadfast_orders.get('note'),
    #                          'created_at': steadfast_orders.get('created_at'),
    #                          'updated_at': steadfast_orders.get('updated_at'),
    #                     })

    #                     # You can logging.info the created record for verification if needed
    #                     logging.info("Steadfast Order created:", steadfast_order)
    #                     logging.info("Data sent successfully to /steadfast route!")
    #          if data.get('status') == 400:
    #                error_message = "Errors during creation of order in SteadFast:\n"
    #                for field, errors in data['errors'].items():
    #                     error_message += f"- {field}: {', '.join(errors)}\n"
    #                # Raise UserError to display the error message as a warning popup
    #                raise ValidationError(error_message)

     def delivey_button(self):
          for order in self:
               print(f"order.company_id.name -------------->{order.company_id.name}")
               steadfast_credentials = self.env["steadfast.credential"].sudo().search([])

               for credential in steadfast_credentials:
                    if credential.company_id.id == order.company_id.id & credential.store_id == order.store_id.id:
                         api_url = credential.api_url
                         api_key = credential.api_key
                         secret_key = credential.secret_key
                         print(f"credential --------------{credential.company_id.name}")

                         invoice = order.name
                         recipient_name = order.partner_id.name
                         recipient_phone = order.partner_id.phone
                         recipient_address = order.partner_id.contact_address
                         cod_amount = order.custom_amount

                         # Make an HTTP POST request to the API route
                         steadfast_credentials = (
                         self.env["steadfast.credential"].sudo().search([])
                         )

                         for credential in steadfast_credentials:
                              api_url = credential.api_url
                              api_key = credential.api_key
                              secret_key = credential.secret_key

                              params = {
                              "invoice": invoice,
                              "recipient_name": recipient_name,
                              "recipient_phone": recipient_phone,
                              "recipient_address": recipient_address,
                              "cod_amount": cod_amount,
                              }
                              response = requests.post(
                              api_url + "/create_order",
                              params=params,
                              headers={
                                   "Content-Type": "application/json",
                                   "Api-Key": api_key,
                                   "Secret-Key": secret_key,
                              },
                              )
                              # Check if the request was successful
                              response.raise_for_status()
                              data = response.json()
                              logging.info(f"response ---------------------------> {data}")
                              if data.get("status") == 400:
                                   error_message = (
                                        "Errors during creation of order in SteadFast:\n"
                                   )
                                   for field, errors in data["errors"].items():
                                        error_message += f"- {field}: {', '.join(errors)}\n"
                                   # Raise UserError to display the error message as a warning popup
                                   raise ValidationError(error_message)

                              if response.status_code == 200:
                                   # Extract relevant information from the response to create the steadfast order record
                                   consignment_info = data.get("consignment")
                                   # Create a record in the steadfast.order model
                                   # Parse datetime strings
                                   created_at = datetime.strptime(
                                        consignment_info.get("created_at"), "%Y-%m-%dT%H:%M:%S.%fZ"
                                   )
                                   updated_at = datetime.strptime(
                                        consignment_info.get("updated_at"), "%Y-%m-%dT%H:%M:%S.%fZ"
                                   )
                                   steadfast_order = self.env["steadfast.order"].create(
                                        {
                                             "consignment_id": consignment_info.get(
                                                  "consignment_id"
                                             ),
                                             "invoice": consignment_info.get("invoice"),
                                             "tracking_code": consignment_info.get("tracking_code"),
                                             "recipient_name": consignment_info.get(
                                                  "recipient_name"
                                             ),
                                             "recipient_phone": consignment_info.get(
                                                  "recipient_phone"
                                             ),
                                             "recipient_address": consignment_info.get(
                                                  "recipient_address"
                                             ),
                                             "cod_amount": consignment_info.get("cod_amount"),
                                             "status": consignment_info.get("status"),
                                             "note": consignment_info.get("note"),
                                             "created_at": created_at.strftime("%Y-%m-%d %H:%M:%S"),
                                             "updated_at": updated_at.strftime("%Y-%m-%d %H:%M:%S"),
                                             "company_id": order.company_id.id,  # Assign company_id from the sale order
                                        }
                                   )

                                   # You can logging.info the created record for verification if needed
                                   logging.info("Steadfast Order created:", steadfast_order)
                                   logging.info("Data sent successfully to /steadfast route!")
                              else:
                                   logging.info(
                                        f"Failed to send data to /steadfast route. Status code: {response.status_code}"
                                   )
