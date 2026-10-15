# trucks/serializers.py
from datetime import date

from rest_framework import serializers

from trucks.models.truck_models import Truck, TruckDocument, TruckInsurance, TruckType


class TruckTypeSerializer(serializers.ModelSerializer):
    """
    Handles serialization and structural capacity metadata definitions
    for freight asset classes.
    """

    class Meta:
        model = TruckType
        fields = [
            "id",
            "name",
            "code",
            "description",
            "max_weight_capacity_kg",
            "max_volume_cubic_meters",
            "length_meters",
            "width_meters",
            "height_meters",
            "axle_count",
            "has_refrigeration",
            "has_tail_lift",
            "is_hazardous_material_certified",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "created_at", "updated_at"]


class TruckDocumentSerializer(serializers.ModelSerializer):
    """
    Manages compliance, permit logs, and safety check files inside the asset vault.
    """

    document_type_display = serializers.CharField(
        source="get_document_type_display", read_only=True
    )

    class Meta:
        model = TruckDocument
        fields = [
            "id",
            "truck",
            "document_type",
            "document_type_display",
            "document_number",
            "file_attachment",
            "expiry_date",
            "is_verified",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "truck", "is_verified", "created_at", "updated_at"]

    def validate_expiry_date(self, value):
        """Ensures compliance certificates are not expired at registration point."""
        if value < date.today():
            raise serializers.ValidationError(
                "The document expiry date cannot be in the past."
            )
        return value


class TruckInsuranceSerializer(serializers.ModelSerializer):
    """
    Maps financial risk coverage frameworks and indemnity caps onto active trucks.
    """

    class Meta:
        model = TruckInsurance
        fields = [
            "id",
            "truck",
            "insurance_provider_name",
            "policy_number",
            "coverage_amount_limit",
            "policy_document",
            "start_date",
            "expiry_date",
            "is_verified",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "truck", "is_verified", "created_at", "updated_at"]

    def validate(self, attrs):
        """Cross-validates operational timelines for coverage policies."""
        start_date = attrs.get("start_date")
        expiry_date = attrs.get("expiry_date")

        if start_date and expiry_date and start_date >= expiry_date:
            raise serializers.ValidationError(
                {
                    "expiry_date": "The insurance policy expiry date must land after the activation start date."
                }
            )

        if expiry_date and expiry_date < date.today():
            raise serializers.ValidationError(
                {"expiry_date": "The insurance policy has already expired."}
            )
        return attrs


class TruckSerializer(serializers.ModelSerializer):
    """
    Comprehensive, nested database model presentation layer compiling deep data structures
    for lists and detail lookups.
    """

    truck_type_details = TruckTypeSerializer(source="truck_type", read_only=True)
    compliance_documents = TruckDocumentSerializer(many=True, read_only=True)
    insurance_policy = TruckInsuranceSerializer(read_only=True)
    driver_name = serializers.CharField(
        source="driver.user.get_full_name", read_only=True
    )
    verification_status_display = serializers.CharField(
        source="get_verification_status_display", read_only=True
    )
    operation_status_display = serializers.CharField(
        source="get_operation_status_display", read_only=True
    )

    class Meta:
        model = Truck
        fields = [
            "id",
            "driver",
            "driver_name",
            "truck_type",
            "truck_type_details",
            "license_plate_number",
            "vin_number",
            "make",
            "model",
            "manufacture_year",
            "primary_color",
            "current_tare_weight_kg",
            "gps_tracker_device_id",
            "verification_status",
            "verification_status_display",
            "operation_status",
            "operation_status_display",
            "is_active",
            "rejection_reason",
            "compliance_documents",
            "insurance_policy",
            "created_at",
            "updated_at",
        ]
        read_only_fields = [
            "id",
            "driver",
            "verification_status",
            "operation_status",
            "is_active",
            "rejection_reason",
            "created_at",
            "updated_at",
        ]


class TruckCreateSerializer(serializers.ModelSerializer):
    """
    Isolated processing sandbox restricting write parameters during truck registration.
    Enforces profile security rules by extracting driver context from token streams.
    """

    class Meta:
        model = Truck
        fields = [
            "id",
            "truck_type",
            "license_plate_number",
            "vin_number",
            "make",
            "model",
            "manufacture_year",
            "primary_color",
            "current_tare_weight_kg",
            "gps_tracker_device_id",
        ]

    def validate_manufacture_year(self, value):
        """Prevents registration of future vehicle assemblies."""
        current_year = date.today().year
        if value > current_year:
            raise serializers.ValidationError(
                f"The manufacture year cannot exceed the current calendar year ({current_year})."
            )
        return value

    def create(self, validated_data):
        """Binds vehicle registries safely onto the executing token driver node profile."""
        request = self.context.get("request")
        if not request or not hasattr(request.user, "driver_profile"):
            raise serializers.ValidationError(
                {
                    "detail": "Authentication profile error: Requesting entity must possess an active Transporter profile."
                }
            )

        validated_data["driver"] = request.user.driver_profile
        # Force default safe compliance values irrespective of raw request bodies
        validated_data["verification_status"] = "PENDING"
        validated_data["operation_status"] = "OFFLINE"
        validated_data["is_active"] = False

        try:
            return super().create(validated_data)
        except Exception as e:
            raise serializers.ValidationError({"database_error": str(e)})
