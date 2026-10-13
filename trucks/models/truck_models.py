import uuid

from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


class TruckType(models.Model):
    """
    Defines classification metrics for available freight assets (e.g., Flatbed, Box Truck, Refrigerated Van, Lowboy).
    Controls filtering indices for cargo configurations and compatibility validations.
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(
        max_length=100,
        unique=True,
        help_text="Common commercial designation of the truck type.",
    )
    code = models.CharField(
        max_length=20,
        unique=True,
        help_text="Standardized lookup code (e.g., REEFER, FLATBED_40FT).",
    )
    description = models.TextField(  # noqa: DJ001
        blank=True,
        null=True,
        help_text="Detailed engineering or operational breakdown of structural limitations.",
    )

    # Maximum Payload & Volume Capacities
    max_weight_capacity_kg = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0.00)],
        help_text="Maximum legal payload threshold in kilograms.",
    )
    max_volume_cubic_meters = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        validators=[MinValueValidator(0.00)],
        blank=True,
        null=True,
        help_text="Usable internal dimensions metric volumetric scale.",
    )

    # External Dimensions
    length_meters = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        blank=True,
        null=True,
        validators=[MinValueValidator(0.00)],
    )
    width_meters = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        blank=True,
        null=True,
        validators=[MinValueValidator(0.00)],
    )
    height_meters = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        blank=True,
        null=True,
        validators=[MinValueValidator(0.00)],
    )

    # Structural Attributes
    axle_count = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(2)],
        default=2,
        help_text="Total active structural support axles.",
    )
    has_refrigeration = models.BooleanField(
        default=False,
        help_text="Denotes functional on-board temperature infrastructure.",
    )
    has_tail_lift = models.BooleanField(
        default=False, help_text="Equipped with mechanical tail gate sorting mechanics."
    )
    is_hazardous_material_certified = models.BooleanField(
        default=False,
        help_text="Structural isolation parameters approved for HAZMAT transports.",
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Truck Type"
        verbose_name_plural = "Truck Types"
        ordering = ["name"]

    def __str__(self):
        return f"{self.name} ({self.max_weight_capacity_kg} kg max)"


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
        "user_profiles.DriverProfile",
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

    def __str__(self):
        return f"{self.make} {self.model} [{self.license_plate_number}]"


class TruckDocument(models.Model):
    """
    Stores critical tracking instances of legality compliance profiles (e.g., Registration cards, Permits, Border clearances).
    """

    class DocumentType(models.TextChoices):
        REGISTRATION = "REGISTRATION", "Vehicle Registration Certificate"
        ROADWORTHINESS = (
            "ROADWORTHINESS",
            "Roadworthiness/Inspection Safety Certificate",
        )
        TRANSIT_PERMIT = "TRANSIT_PERMIT", "Commercial Cross-Border Goods Permit"
        WEIGHT_CERTIFICATE = "WEIGHT_CERTIFICATE", "Certified Weight Bridge Slip"
        OTHER = "OTHER", "Supplementary Compliance Form"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    truck = models.ForeignKey(
        Truck, on_delete=models.CASCADE, related_name="compliance_documents"
    )

    document_type = models.CharField(max_length=30, choices=DocumentType.choices)
    document_number = models.CharField(
        max_length=100,
        help_text="The reference sequence identifier printed directly on the physical document asset.",
    )
    file_attachment = models.FileField(
        upload_to="trucks/compliance_vault/",
        help_text="Secure binary file location handling active cloud uploads safely.",
    )

    expiry_date = models.DateField(
        help_text="Calendar boundary warning systems calculations checkpoint tracking fields."
    )
    is_verified = models.BooleanField(
        default=False, help_text="System-level validation confirmation marker toggle."
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Truck Document"
        verbose_name_plural = "Truck Documents"
        ordering = ["-expiry_date"]

    def __str__(self):
        return f"{self.get_document_type_display()} for Truck: {self.truck.license_plate_number}"


class TruckInsurance(models.Model):
    """
    Manages operational commercial cargo/liability transit coverage policies tied to physical tracking assets.
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    truck = models.OneToOneField(
        Truck, on_delete=models.CASCADE, related_name="insurance_policy"
    )

    insurance_provider_name = models.CharField(
        max_length=150, help_text="Underwriting corporate legal brand entity label."
    )
    policy_number = models.CharField(
        max_length=100,
        unique=True,
        help_text="Unique contract binder registration key reference.",
    )
    coverage_amount_limit = models.DecimalField(
        max_digits=14,
        decimal_places=2,
        validators=[MinValueValidator(0.00)],
        help_text="Maximum financial recovery liability coverage scale assigned to active claims parameters.",
    )

    policy_document = models.FileField(upload_to="trucks/insurance_vault/")
    start_date = models.DateField(
        help_text="Activation boundary point calendar metric dates."
    )
    expiry_date = models.DateField(
        help_text="Critical platform trip deployment disqualification expiration index calculation target."
    )
    is_verified = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Truck Insurance"
        verbose_name_plural = "Truck Insurances"

    def __str__(self):
        return f"Policy {self.policy_number} ({self.insurance_provider_name})"
