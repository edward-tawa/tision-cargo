import requests
from django.conf import settings
from loguru import logger

class EcoCashPaymentService:
    def __init__(self):
        self.api_url = getattr(settings, "ECOCASH_API_URL", "https://api.ecocash.co.zw/v1/merchant/transaction")
        self.merchant_id = getattr(settings, "ECOCASH_MERCHANT_ID", "DUMMY_ID")
        self.api_key = getattr(settings, "ECOCASH_API_KEY", "DUMMY_KEY")

    def _get_headers(self) -> dict:
        return {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "Accept": "application/json"
        }

    def initiate_ussd_push(self, ecocash_number: str, amount: float, currency: str, reference: str) -> dict:
        payload = {
            "merchantId": self.merchant_id,
            "subscriberNumber": ecocash_number,
            "amount": float(amount),
            "currency": currency,
            "clientCorrelator": reference,
            "merchantReference": reference,
        }
        
        try:
            logger.info(f"Dispatching EcoCash USSD Push to {ecocash_number} for ref: {reference}")
            response = requests.post(self.api_url, json=payload, headers=self._get_headers(), timeout=30)
            
            if response.status_code in [200, 201]:
                return {"success": True, "data": response.json()}
            
            logger.error(f"EcoCash Gateway Rejected Request. Status: {response.status_code}, Body: {response.text}")
            return {"success": False, "error": f"Gateway error ({response.status_code}): {response.text}"}
            
        except requests.exceptions.Timeout:
            logger.error(f"Timeout connecting to EcoCash Interface Engine for trace ref: {reference}")
            return {"success": False, "error": "EcoCash service timed out. Please try again."}
        except requests.exceptions.RequestException as e:
            logger.exception("Failed executing network operation against EcoCash server.")
            return {"success": False, "error": f"Network transmission fault: {str(e)}"}
