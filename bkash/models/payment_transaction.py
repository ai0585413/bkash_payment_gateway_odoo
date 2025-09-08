from odoo import models, fields, _
import requests

class PaymentTransactionBkash(models.Model):
    _inherit = 'payment.transaction'

    bkash_payment_id = fields.Char("bKash Payment ID")

    def _get_specific_rendering_values(self, processing_values):
        """Create payment with bKash"""
        res = super()._get_specific_rendering_values(processing_values)
        if self.provider_code != 'bkash':
            return res

        provider = self.provider_id
        token = provider._bkash_get_token()

        url = f"{provider.bkash_base_url}/tokenized/checkout/create"
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Authorization": f"Bearer {token}",
            "X-APP-Key": provider.bkash_app_key
        }
        payload = {
            "mode": "0000",
            "payerReference": "ODooCustomer",
            "callbackURL": f"{provider.get_base_url()}/payment/bkash/return",
            "amount": str(self.amount),
            "currency": self.currency_id.name,
            "intent": "sale",
            "merchantInvoiceNumber": self.reference
        }

        response = requests.post(url, json=payload, headers=headers, timeout=20).json()
        self.bkash_payment_id = response.get("paymentID")
        return {'redirect_url': response.get("bkashURL")}
