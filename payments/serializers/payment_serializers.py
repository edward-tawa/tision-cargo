import re
from rest_framework import serializers
from payments.models.payment_models import Transaction

class InitiatePaymentSerializer(serializers.Serializer):
    ecocash_number = serializers.CharField(max_length=15)
    amount = serializers.DecimalField(max_digits=10, decimal_places=2, min_value=0.01)
    currency = serializers.ChoiceField(choices=["ZWG", "USD"], default="ZWG")

    def validate_ecocash_number(self, value):
        clean_value = re.sub(r'\s+|-', '', value)
        pattern = r'^(\+?263|0)(77|78)\d{7}$'
        if not re.match(pattern, clean_value):
            raise serializers.ValidationError("Invalid EcoCash Phone Number format. Must be an active Econet line.")
        return clean_value


class TransactionDetailSerializer(serializers.ModelSerializer):
    driver_name = serializers.CharField(source="driver.get_full_name", read_only=True)

    class Meta:
        model = Transaction
        fields = [
            "id", "driver", "driver_name", "ecocash_number", 
            "client_correlator", "correlator_id", "amount", 
            "currency", "status", "failure_reason", "created_at"
        ]
        read_only_fields = fields


class EcoCashWebhookSerializer(serializers.Serializer):
    clientCorrelator = serializers.CharField(max_length=100)
    correlatorId = serializers.CharField(max_length=100, required=False, allow_blank=True)
    transactionStatus = serializers.ChoiceField(choices=["COMPLETED", "FAILED", "DECLINED", "TIMEOUT"])
    rawPayload = serializers.JSONField(required=False, default=dict)
    reason = serializers.CharField(required=False, allow_blank=True)
