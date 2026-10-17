import uuid
from django.db import models
from django.conf import settings

class TransactionStatus(models.TextChoices):
    PENDING = "PENDING", "Pending Subscriber Action"
    SUCCESSFUL = "SUCCESSFUL", "Completed Successfully"
    FAILED = "FAILED", "Failed/Declined Transaction"
    EXPIRED = "EXPIRED", "USSD Push Timeout"


class Transaction(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    driver = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="payments",
        help_text="The Driver user entity discharging this payment."
    )
    ecocash_number = models.CharField(max_length=15, db_index=True, help_text="EcoCash wallet string format (e.g. 077XXXXXXX)")
    correlator_id = models.CharField(max_length=100, unique=True, null=True, blank=True, help_text="EcoCash Gateway Reference identifier")
    client_correlator = models.CharField(max_length=100, unique=True, db_index=True, help_text="Internal unique trace string reference")
    
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=3, default="ZWG", help_text="ISO Currency Code (e.g., ZWG or USD)")
    status = models.CharField(
        max_length=20,
        choices=TransactionStatus.choices,
        default=TransactionStatus.PENDING,
        db_index=True
    )
    
    raw_api_payload = models.JSONField(default=dict, blank=True, help_text="Saves complete vendor response payload history")
    failure_reason = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]
        permissions = [
            ("can_initiate_payment", "Can initiate a payment flow"),
            ("can_refund_transaction", "Can reverse or refund an entry"),
            ("can_view_analytics", "Can view system-wide payment charts"),
        ]

    def __str__(self):
        return f"TXN-{self.id} | {self.driver.username} | {self.amount} {self.currency} ({self.status})"
