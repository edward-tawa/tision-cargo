import uuid
from django.db import transaction
from django.db.models import Sum, Count
from rest_framework import viewsets, status
from rest_framework.decorators import action

from core.api_responses.responses import success_response, error_response
from payments.permissions.payment_permissions import PaymentAppPermission
from payments.models.payment_models import Transaction, TransactionStatus
from payments.serializers.payment_serializers import (
    InitiatePaymentSerializer, 
    TransactionDetailSerializer, 
    EcoCashWebhookSerializer
)
from payments.services.ecocash_service import EcoCashPaymentService


class PaymentViewSet(viewsets.ModelViewSet):
    queryset = Transaction.objects.all()
    permission_classes = [PaymentAppPermission]
    
    def get_serializer_class(self):
        if self.action == "initiate_payment":
            return InitiatePaymentSerializer
        return TransactionDetailSerializer

    def get_queryset(self):
        user = self.request.user
        if user.is_staff or user.groups.filter(name="admin").exists():
            return self.queryset
        return self.queryset.filter(driver=user)

    @action(detail=False, methods=["post"], url_path="initiate")
    def initiate_payment(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        validated_data = serializer.validated_data
        client_ref = f"HWL-{uuid.uuid4().hex[:12].upper()}"

        txn = Transaction.objects.create(
            driver=request.user,
            ecocash_number=validated_data["ecocash_number"],
            amount=validated_data["amount"],
            currency=validated_data["currency"],
            client_correlator=client_ref,
            status=TransactionStatus.PENDING
        )

        service = EcoCashPaymentService()
        result = service.initiate_ussd_push(
            ecocash_number=txn.ecocash_number,
            amount=txn.amount,
            currency=txn.currency,
            reference=client_ref
        )

        if result["success"]:
            api_data = result["data"]
            txn.correlator_id = api_data.get("correlatorId")
            txn.raw_api_payload = api_data
            txn.save()

            return success_response(
                message="USSD push successfully broadcast to subscriber mobile terminal. Please confirm with your PIN.",
                status=status.HTTP_201_CREATED,
                data=TransactionDetailSerializer(txn).data
            )
        else:
            txn.status = TransactionStatus.FAILED
            txn.failure_reason = result["error"]
            txn.save()

            return error_response(
                message="EcoCash initialization failure occurred.",
                status=status.HTTP_424_FAILED_DEPENDENCY,
                errors={"detail": result["error"]}
            )

    @action(detail=False, methods=["post"], url_path="webhook", authentication_classes=[], permission_classes=[])
    def webhook_callback(self, request):
        serializer = EcoCashWebhookSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        data = serializer.validated_data
        ref = data["clientCorrelator"]

        try:
            with transaction.atomic():
                txn = Transaction.objects.select_for_update().get(client_correlator=ref)
                
                if txn.status != TransactionStatus.PENDING:
                    return success_response(message="Transaction already settled.", status=status.HTTP_200_OK)

                status_map = {
                    "COMPLETED": TransactionStatus.SUCCESSFUL,
                    "FAILED": TransactionStatus.FAILED,
                    "DECLINED": TransactionStatus.FAILED,
                    "TIMEOUT": TransactionStatus.EXPIRED,
                }
                
                txn.status = status_map.get(data["transactionStatus"], TransactionStatus.FAILED)
                if data.get("correlatorId"):
                    txn.correlator_id = data["correlatorId"]
                if data.get("reason"):
                    txn.failure_reason = data["reason"]
                
                txn.raw_api_payload = data.get("rawPayload", {})
                txn.save()
                
            return success_response(message="Status update acknowledged.", status=status.HTTP_200_OK)
            
        except Transaction.DoesNotExist:
            return error_response(
                message="Matching transaction reference not found.",
                status=status.HTTP_404_NOT_FOUND
            )

    @action(detail=False, methods=["get"], url_path="analytics")
    def analytics(self, request):
        metrics = self.get_queryset().values("status").annotate(
            total_amount=Sum("amount"),
            transaction_count=Count("id")
        )
        return success_response(
            message="Aggregated accounting logs compiled successfully.",
            status=status.HTTP_200_OK,
            data={"metrics": list(metrics)}
        )
