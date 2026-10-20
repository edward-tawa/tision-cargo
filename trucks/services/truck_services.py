# trucks/services.py
from datetime import date, timedelta

from django.db import transaction
from loguru import logger
from rest_framework.exceptions import PermissionDenied, ValidationError

# Core App Architectures & Modules Integrations
# (Derived from custom responses, exception handlers, and user systems)
from core.exceptions.custom_exception_handler import custom_exception_handler
from trucks.models.truck_document_model import TruckDocument
from trucks.models.truck_insurance_model import TruckInsurance
from trucks.models.truck_model import Truck


class TruckComplianceService:
    """
    Domain service executing workflow evaluations regarding vehicle tracking assets,
    compliance states, auditing validation cycles, and operation visibility.
    """

    @staticmethod
    def evaluate_truck_eligibility(truck: Truck) -> bool:
        """
        Evaluates a vehicle's compliance parameters across multiple validation layers.
        If any critical policy document is missing or expired, the vehicle is automatically
        flagged as unverified or non-operational.
        """
        today = date.today()

        # 1. Base platform status checks
        if (
            not truck.is_active
            or truck.verification_status != Truck.VerificationStatus.APPROVED
        ):
            return False

        # 2. Check for active insurance policy layout parameters
        try:
            insurance = truck.insurance_policy
            if not insurance.is_verified or insurance.expiry_date <= today:
                logger.warning(
                    "Truck {} failed compliance audit: Insurance configuration expired or unverified.",
                    truck.id,
                )
                return False
        except TruckInsurance.DoesNotExist:
            logger.warning(
                "Truck {} failed compliance audit: No associated insurance policy structure found.",
                truck.id,
            )
            return False

        # 3. Check for mandatory operational verification documents
        mandatory_docs = [
            TruckDocument.DocumentType.REGISTRATION,
            TruckDocument.DocumentType.ROADWORTHINESS,
        ]

        active_docs = truck.compliance_documents.filter(
            document_type__in=mandatory_docs, is_verified=True, expiry_date__gt=today
        )

        # Ensure all types of mandatory documents are actively registered and valid
        found_types = {doc.document_type for doc in active_docs}
        if len(found_types) < len(mandatory_docs):
            logger.warning(
                "Truck {} failed compliance audit: Missing required verified documents {}.",
                truck.id,
                mandatory_docs,
            )
            return False

        return True

    @classmethod
    @transaction.atomic
    def process_daily_compliance_audit(cls) -> dict:
        """
        System-wide periodic worker service (e.g., Celery target) scanning active fleets
        to identify and isolate newly expired documents or insurance policies.
        """
        today = date.today()
        summary = {
            "suspended_trucks": 0,
            "flagged_documents": 0,
            "flagged_insurance": 0,
        }

        try:
            # Unverify expired documents
            expired_docs = TruckDocument.objects.filter(
                is_verified=True, expiry_date__lte=today
            )
            summary["flagged_documents"] = expired_docs.count()
            expired_docs.update(is_verified=False)

            # Unverify expired insurance policies
            expired_insurance = TruckInsurance.objects.filter(
                is_verified=True, expiry_date__lte=today
            )
            summary["flagged_insurance"] = expired_insurance.count()
            expired_insurance.update(is_verified=False)

            # Sweep and suspend trucks that no longer pass compliance checks
            active_fleet = Truck.objects.filter(
                is_active=True, verification_status=Truck.VerificationStatus.APPROVED
            )

            for truck in active_fleet:
                if not cls.evaluate_truck_eligibility(truck):
                    truck.verification_status = Truck.VerificationStatus.SUSPENDED
                    truck.operation_status = Truck.OperationStatus.OFFLINE
                    truck.rejection_reason = "Automated core compliance audit: Required documentation or coverage expired."
                    truck.save()
                    summary["suspended_trucks"] += 1
                    logger.info(
                        "Truck ID {} has been SUSPENDED automatically due to data expiration loops.",
                        truck.id,
                    )

        except Exception as exc:
            # Route unhandled batch issues through the core custom exception processing layout
            logger.error(
                "Core daily compliance audit service step failed structurally."
            )
            custom_exception_handler(
                exc, context={"view": "AutomatedComplianceAuditTask"}
            )
            raise exc

        return summary


class TruckTelemetryService:
    """
    Handles real-time status transitions, tracking state modifications,
    and device mapping telemetry hooks for individual fleet nodes.
    """

    @staticmethod
    def transition_operation_status(
        truck_id: str, target_status: str, operator_user
    ) -> Truck:
        """
        Safely transitions a vehicle's operational state with safety validation boundaries.
        Prevents unverified, suspended, or under-insured vehicles from going 'AVAILABLE' or 'ON_TRIP'.
        """
        truck = Truck.objects.select_related("insurance_policy", "driver__user").get(
            id=truck_id
        )

        # Enforce multi-tenant resource layer security using standard DRF exceptions
        if operator_user.role == "DRIVER" and truck.driver.user != operator_user:
            logger.error(
                "Unauthorized access breach attempt: User {} on Truck {}",
                operator_user.id,
                truck.id,
            )
            raise PermissionDenied(
                "Access Denied: You do not possess operational tracking authority over this fleet unit."
            )

        if target_status in [
            Truck.OperationStatus.AVAILABLE,
            Truck.OperationStatus.ON_TRIP,
        ]:
            # Trigger real-time deep structural compliance evaluation checks
            is_eligible = TruckComplianceService.evaluate_truck_eligibility(truck)
            if not is_eligible:
                raise ValidationError(
                    f"Transition to status '{target_status}' rejected. This vehicle is missing verified insurance or registration documentation."
                )

        truck.operation_status = target_status
        truck.save()
        logger.info(
            "User {} updated Truck {} operation status matrix to {}.",
            operator_user.id,
            truck.id,
            target_status,
        )
        return truck

    @staticmethod
    def register_gps_hardware(truck_id: str, imei_string: str) -> Truck:
        """
        Binds a custom telematics physical device tracking IMEI string directly onto a registered truck asset node.
        """
        if (
            Truck.objects.filter(gps_tracker_device_id=imei_string)
            .exclude(id=truck_id)
            .exists()
        ):
            raise ValidationError(
                {
                    "gps_tracker_device_id": "This tracking hardware identifier is already mapped onto an active vehicle configuration."
                }
            )

        truck = Truck.objects.get(id=truck_id)
        truck.gps_tracker_device_id = imei_string
        truck.save()
        logger.info(
            "GPS hardware node validation loop mapped tracker data onto Truck ID {}",
            truck_id,
        )
        return truck


class NotificationAlertService:
    """
    Utility service coordinating structural platform triggers to notify system entities when documents approach expiration.
    """

    @staticmethod
    def dispatch_expiry_warnings(warning_window_days: int = 7) -> int:
        """
        Scans compliance databases to look for upcoming document or policy timeouts,
        generating alerts for operators via the core application notification framework.
        """
        target_date = date.today() + timedelta(days=warning_window_days)
        alert_count = 0

        # Query upcoming structural documentation drops
        expiring_docs = TruckDocument.objects.filter(
            expiry_date=target_date, is_verified=True
        ).select_related("truck__driver__user")

        for doc in expiring_docs:
            user = doc.truck.driver.user
            message_body = f"Your truck document ({doc.get_document_type_display()}) # {doc.document_number} expires in {warning_window_days} days. Please upload updated credentials to stay eligible for cargo routing."

            # Using lazy execution patterns for core models to prevent cyclical dependency chains
            from django.apps import apps

            try:
                NotificationModel = apps.get_model("notifications", "Notification")
                NotificationModel.objects.create(
                    user=user,
                    title="Compliance Action Required: Document Expiry",
                    body=message_body,
                    is_seen=False,
                )
                logger.info(
                    "Dispatched system warning alert data model entry to User {} regarding document expiration.",
                    user.id,
                )
                alert_count += 1
            except (LookupError, ValueError):
                # Fallback to structural logs if the communications/notifications app isn't initialized yet
                logger.warning(
                    "Notification module abstract database target unreached. Falling back to log trace: Warning for user email: {}",
                    user.email,
                )
                alert_count += 1

        return alert_count
