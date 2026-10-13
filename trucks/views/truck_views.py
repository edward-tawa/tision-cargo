# trucks/views.py
from django.shortcuts import get_object_or_404
from loguru import logger
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import PermissionDenied, ValidationError

# Core App Module Integrations
from core.api_responses.responses import success_response
from core.permissions.core_permissions import CorePermission

# Local App Architecture Components
from trucks.models.truck_models import Truck, TruckType
from trucks.serializers.truck_serializer import (
    TruckCreateSerializer,
    TruckDocumentSerializer,
    TruckInsuranceSerializer,
    TruckSerializer,
    TruckTypeSerializer,
)
from trucks.services.truck_services import TruckTelemetryService


class TruckPermission(CorePermission):
    """
    Granular action-to-permission mapping for the trucks application resource endpoints,
    extending the core custom RBAC permission framework.
    """

    permissions_map = {
        "list": ["trucks.view_truck"],
        "retrieve": ["trucks.view_truck"],
        "create": ["trucks.add_truck"],
        "update": ["trucks.change_truck"],
        "partial_update": ["trucks.change_truck"],
        "destroy": ["trucks.delete_truck"],
        "update_status": ["trucks.can_change_truck_status"],
        "verify_truck": ["trucks.can_verify_truck"],
        "upload_document": ["trucks.add_truckdocument"],
        "add_insurance": ["trucks.add_truckinsurance"],
        "active_fleet": ["trucks.view_truck"],
    }


class TruckViewSet(viewsets.ModelViewSet):
    """
    Resourceful ModelViewSet executing complete lifecycle administration, compliance auditing,
    telemetry management, and validation over the Truck ecosystem.
    """

    queryset = Truck.objects.select_related(
        "driver__user", "truck_type"
    ).prefetch_related("compliance_documents", "insurance_policy")
    permission_classes = [TruckPermission]

    def get_serializer_class(self):
        """Dynamically switches serializers based on write/read workloads."""
        if self.action == "create":
            return TruckCreateSerializer
        return TruckSerializer

    def list(self, request, *args, **kwargs):
        """
        Retrieve a list of trucks, filtered by role and tenancy restrictions.
        Drivers only see their own fleet; Admins maintain global oversight.
        """
        user = request.user
        queryset = self.get_queryset()

        if user.role == "DRIVER":
            if not hasattr(user, "driver_profile"):
                raise PermissionDenied("Missing active transporter driver profile.")
            queryset = queryset.filter(driver=user.driver_profile)

        page = self.paginate_queryset(queryset)
        serializer = (
            self.get_serializer(page, many=True)
            if page is not None
            else self.get_serializer(queryset, many=True)
        )

        data = (
            self.get_paginated_response(serializer.data).data
            if page is not None
            else serializer.data
        )
        return success_response(
            message="Trucks registry retrieved successfully.",
            status=status.HTTP_200_OK,
            data=data,
        )

    def retrieve(self, request, pk=None, *args, **kwargs):
        """
        Retrieve detailed information for a specific truck resource asset.
        """
        user = request.user
        queryset = self.get_queryset()

        if user.role == "DRIVER":
            if not hasattr(user, "driver_profile"):
                raise PermissionDenied("Missing active transporter driver profile.")
            queryset = queryset.filter(driver=user.driver_profile)

        truck = get_object_or_404(queryset, pk=pk)
        serializer = self.get_serializer(truck)
        return success_response(
            message="Truck resource detail fetched successfully.",
            status=status.HTTP_200_OK,
            data=serializer.data,
        )

    def create(self, request, *args, **kwargs):
        """
        Register a new truck resource asset and link it to the requesting driver profile.
        """
        serializer = self.get_serializer(
            data=request.data, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        truck = serializer.save()

        # Read back using full presentation schema
        read_serializer = TruckSerializer(truck)
        return success_response(
            message="Truck asset registered successfully and awaiting verification compliance checks.",
            status=status.HTTP_201_CREATED,
            data=read_serializer.data,
        )

    def update(self, request, pk=None, *args, **kwargs):
        """
        Update complete configuration profiles for an existing truck entry.
        """
        user = request.user
        queryset = self.get_queryset()

        if user.role == "DRIVER":
            if not hasattr(user, "driver_profile"):
                raise PermissionDenied("Missing active transporter driver profile.")
            queryset = queryset.filter(driver=user.driver_profile)

        truck = get_object_or_404(queryset, pk=pk)
        serializer = self.get_serializer(truck, data=request.data, partial=False)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return success_response(
            message="Truck asset configurations updated successfully.",
            status=status.HTTP_200_OK,
            data=serializer.data,
        )

    def partial_update(self, request, pk=None, *args, **kwargs):
        """
        Patch isolated properties of a targeted truck model configuration.
        """
        user = request.user
        queryset = self.get_queryset()

        if user.role == "DRIVER":
            if not hasattr(user, "driver_profile"):
                raise PermissionDenied("Missing active transporter driver profile.")
            queryset = queryset.filter(driver=user.driver_profile)

        truck = get_object_or_404(queryset, pk=pk)
        serializer = self.get_serializer(truck, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return success_response(
            message="Truck asset components modified successfully.",
            status=status.HTTP_200_OK,
            data=serializer.data,
        )

    def destroy(self, request, pk=None, *args, **kwargs):
        """
        Remove a truck configuration block from active operational pools.
        """
        user = request.user
        queryset = self.get_queryset()

        if user.role == "DRIVER":
            if not hasattr(user, "driver_profile"):
                raise PermissionDenied("Missing active transporter driver profile.")
            queryset = queryset.filter(driver=user.driver_profile)

        truck = get_object_or_404(queryset, pk=pk)
        truck.delete()
        logger.info(
            "Truck ID {} completely purged from database registry by User {}",
            pk,
            user.id,
        )

        return success_response(
            message="Truck asset record completely unlinked and removed from database.",
            status=status.HTTP_200_OK,
        )

    @action(detail=True, methods=["patch"], url_path="update-status")
    def update_status(self, request, pk=None):
        """
        Toggle telemetry operational phase matrices for a given asset (AVAILABLE, ON_TRIP, OFFLINE, MAINTENANCE)
        via the domain layer telemetry service safely.
        """
        target_status = request.data.get("operation_status")
        if not target_status:
            raise ValidationError({"operation_status": "This field is required."})

        # Process through business logic layer to run state-machine guard constraints
        truck = TruckTelemetryService.transition_operation_status(
            truck_id=pk, target_status=target_status, operator_user=request.user
        )

        return success_response(
            message=f"Truck status successfully moved to {target_status}.",
            status=status.HTTP_200_OK,
            data={"id": truck.id, "operation_status": truck.operation_status},
        )

    @action(detail=True, methods=["post"], url_path="verify")
    def verify_truck(self, request, pk=None):
        """
        Administrative compliance checkpoint to sign off, flag, or reject registered vehicles.
        """
        truck = get_object_or_404(Truck, pk=pk)
        verification_value = request.data.get("verification_status")
        rejection_reason = request.data.get("rejection_reason", "")

        if verification_value not in [
            Truck.VerificationStatus.APPROVED,
            Truck.VerificationStatus.REJECTED,
        ]:
            raise ValidationError(
                {
                    "verification_status": f"Must be set explicitly to {Truck.VerificationStatus.APPROVED} or {Truck.VerificationStatus.REJECTED}."
                }
            )

        truck.verification_status = verification_value
        if verification_value == Truck.VerificationStatus.APPROVED:
            truck.is_active = True
            truck.rejection_reason = None
        else:
            truck.is_active = False
            truck.operation_status = Truck.OperationStatus.OFFLINE
            truck.rejection_reason = rejection_reason

        truck.save()
        logger.info(
            "Administrative audit updated Truck {} verification matrix to {}",
            truck.id,
            verification_value,
        )

        return success_response(
            message=f"Truck asset review completed. Result: {verification_value}.",
            status=status.HTTP_200_OK,
            data={
                "id": truck.id,
                "verification_status": truck.verification_status,
                "is_active": truck.is_active,
                "operation_status": truck.operation_status,
            },
        )

    @action(detail=True, methods=["post"], url_path="upload-document")
    def upload_document(self, request, pk=None):
        """
        Direct inline execution attachment point to upload compliance/roadworthiness documentation files.
        """
        user = request.user
        queryset = Truck.objects.all()
        if user.role == "DRIVER":
            queryset = queryset.filter(driver__user=user)

        truck = get_object_or_404(queryset, pk=pk)

        serializer = TruckDocumentSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(truck=truck)

        return success_response(
            message="Compliance verification document securely committed to validation vault storage.",
            status=status.HTTP_201_CREATED,
            data=serializer.data,
        )

    @action(detail=True, methods=["post"], url_path="add-insurance")
    def add_insurance(self, request, pk=None):
        """
        Direct entry point to assign a distinct coverage policy tracking ledger to a vehicle profile.
        """
        user = request.user
        queryset = Truck.objects.all()
        if user.role == "DRIVER":
            queryset = queryset.filter(driver__user=user)

        truck = get_object_or_404(queryset, pk=pk)

        # Check if policy already exists to enforce OneToOne structure handling gracefully
        if hasattr(truck, "insurance_policy"):
            raise ValidationError(
                {
                    "detail": "An insurance policy structure already exists for this vehicle. Please update the existing entry."
                }
            )

        serializer = TruckInsuranceSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(truck=truck)

        return success_response(
            message="Commercial policy liability structure safely linked to requested vehicle profile.",
            status=status.HTTP_201_CREATED,
            data=serializer.data,
        )

    @action(detail=False, methods=["get"], url_path="active-fleet")
    def active_fleet(self, request):
        """
        Global open access endpoint tracking active, approved, and currently available transport fleet units.
        """
        active_units = self.get_queryset().filter(
            is_active=True,
            verification_status=Truck.VerificationStatus.APPROVED,
            operation_status=Truck.OperationStatus.AVAILABLE,
        )

        page = self.paginate_queryset(active_units)
        serializer = (
            self.get_serializer(page, many=True)
            if page is not None
            else self.get_serializer(active_units, many=True)
        )

        data = (
            self.get_paginated_response(serializer.data).data
            if page is not None
            else serializer.data
        )
        return success_response(
            message="Available public transportation asset units retrieved.",
            status=status.HTTP_200_OK,
            data=data,
        )


class TruckTypeViewSet(viewsets.ReadOnlyModelViewSet):
    """
    System lookup directory detailing truck cargo configurations and structural load boundaries.
    """

    queryset = TruckType.objects.all()
    serializer_class = TruckTypeSerializer
    permission_classes = [
        CorePermission
    ]  # Defaults to general view access for authenticated users

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return success_response(
            message="Truck classifications configuration indices pulled.",
            status=status.HTTP_200_OK,
            data=serializer.data,
        )

    def retrieve(self, request, pk=None, *args, **kwargs):
        truck_type = get_object_or_404(self.get_queryset(), pk=pk)
        serializer = self.get_serializer(truck_type)
        return success_response(
            message="Truck classification parameters loaded.",
            status=status.HTTP_200_OK,
            data=serializer.data,
        )
