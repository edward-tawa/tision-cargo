from core.permissions.permissions import CorePermission

class PaymentAppPermission(CorePermission):
    permissions_map = {
        "initiate_payment": ["payments.can_initiate_payment"],
        "list": ["payments.view_transaction"],
        "retrieve": ["payments.view_transaction"],
        "webhook_callback": [],
        "analytics": ["payments.can_view_analytics"]
    }
