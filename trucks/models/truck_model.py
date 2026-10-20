import uuid

from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from trucks.models.truck_type_model import TruckType


class Truck(models.Model):
    """
    Represents an isolated physical vehicle fleet entity deployed onto the platform.
    Linked closely to verification layers and real-time operational availability matrix parameters.
    """

    class VerificationStatus(models.TextChoices):
        PENDING = "PENDING", "Pending Verification"
        APPROVED = "APPROVED", "Approved for Active Trips"
        REJECTED = "REJECTED", "Rejected/Compliance Failure"
        SUSPENDED = "SUSPENDED", "Temporarily Suspended"

    class OperationStatus(models.TextChoices):
        OFFLINE = "OFFLINE", "Offline / Non-Operational"
        AVAILABLE = "AVAILABLE", "Available for Instant Booking / Bidding"
        ON_TRIP = "ON_TRIP", "En Route / Active Trip Engagement"
        MAINTENANCE = "MAINTENANCE", "In Shop / Scheduled Maintenance"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    # Relationships (Assuming 'drivers' app manages the Driver proxy model)
    driver = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="registered_trucks",
        help_text="Primary operator or company-level owner node assignment.",
    )
    truck_type = models.ForeignKey(
        TruckType,
        on_delete=models.PROTECT,
        related_name="associated_fleet_vehicles",
        help_text="Underlying structural capacity layout blueprint classification.",
    )

    # Core Identifiers
    license_plate_number = models.CharField(
        max_length=30,
        unique=True,
        help_text="State or country legal registration plate reference string.",
    )
    vin_number = models.CharField(
        max_length=50,
        unique=True,
        verbose_name="VIN/Chassis Number",
        help_text="Unique verified Vehicle Identification Number string.",
    )
    make = models.CharField(
        max_length=60,
        help_text="Manufacturer brand profile identifier (e.g., Volvo, Scania, Isuzu, Freightliner).",
    )
    model = models.CharField(
        max_length=80, help_text="Manufacturer product model designation index line."
    )
    manufacture_year = models.PositiveIntegerField(
        validators=[MinValueValidator(1900), MaxValueValidator(2100)],
        help_text="Calendar year matching assembly output lines.",
    )
    primary_color = models.CharField(  # noqa: DJ001
        max_length=30,
        blank=True,
        null=True,
        help_text="Visual identifying exterior profile color.",
    )

    # Structural Asset Configuration Variables
    current_tare_weight_kg = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0.00)],
        help_text="Empty curb vehicle operating mass weight context metric.",
    )
    gps_tracker_device_id = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        unique=True,
        help_text="Hardware registration IMEI string mapping live telemetry streams.",
    )

    # Compliance & Platform State Audits
    verification_status = models.CharField(
        max_length=20,
        choices=VerificationStatus.choices,
        default=VerificationStatus.PENDING,
    )
    operation_status = models.CharField(
        max_length=20, choices=OperationStatus.choices, default=OperationStatus.OFFLINE
    )
    is_active = models.BooleanField(
        default=True,
        help_text="Global soft-deletion indicator switch tool profile toggle.",
    )
    rejection_reason = models.TextField(  # noqa: DJ001
        blank=True,
        null=True,
        help_text="Compliance audit logging trace tracking metadata errors on document rejection profiles.",
    )

    # Time tracking variables
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Truck"
        verbose_name_plural = "Trucks"
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["license_plate_number"]),
            models.Index(fields=["verification_status"]),
            models.Index(fields=["operation_status"]),
        ]

        permissions = [
            ("can_add_truck", "Can add a new truck"),
            ("can_update_truck", "Can update truck details"),
            ("can_delete_truck", "Can delete a truck"),
            ("can_verify_truck", "Can verify truck compliance"),
            ("can_change_truck_status", "Can change truck operational status"),
            ("can_create_truck", "Can create a truck"),
            ("can_read_truck", "Can read truck details"),
        ]

    def __str__(self):
        return f"{self.make} {self.model} [{self.license_plate_number}]"
