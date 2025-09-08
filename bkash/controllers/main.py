from odoo import http
from odoo.http import request
import requests

class BkashController(http.Controller):

    @http.route(['/payment/bkash/return'], type='http', auth='public', csrf=False)
    def bkash_return(self, **post):
        payment_id = post.get("paymentID")
        status = post.get("status")

        tx = request.env['payment.transaction'].sudo().search([('bkash_payment_id', '=', payment_id)], limit=1)
        provider = tx.provider_id

        if status == "success":
            token = provider._bkash_get_token()
            url = f"{provider.bkash_base_url}/tokenized/checkout/execute"
            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {token}",
                "X-APP-Key": provider.bkash_app_key
            }
            payload = {"paymentID": payment_id}
            response = requests.post(url, json=payload, headers=headers, timeout=20).json()

            tx._set_done()  # Mark transaction successful
            return request.redirect('/payment/status')

        elif status == "failure":
            tx._set_error("bKash payment failed")
        elif status == "cancel":
            tx._set_canceled()
        return request.redirect('/payment/status')
