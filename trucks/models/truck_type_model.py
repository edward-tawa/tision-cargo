import uuid

from django.core.validators import MinValueValidator
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
