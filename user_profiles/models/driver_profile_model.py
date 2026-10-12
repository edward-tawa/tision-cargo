from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from core.models.time_stamp_model import TimeStampModel


class DriverProfile(TimeStampModel):
    """
    Profile model for system drivers.
    Primary key is explicitly inherited from the Common User model.
    """

    class VehicleType(models.TextChoices):
        PICKUP = "PICKUP", "Pickup truck 1 tonne"
        TRUCK_3T = "3_TONNE", "3 Tonne truck"
        TRUCK_5T = "5_TONNE", "5 Tonne truck"
        TRUCK_7T = "7_TONNE", "7 Tonne truck"
        TIPPER = "TIPPER", "Tipper truck"

    # primary_key=True makes this field the actual PK of this table, matching the User's ID
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        primary_key=True,
        related_name="driver_profile",
    )

    drivers_license_number = models.CharField(max_length=50, unique=True, db_index=True)

    vehicle_type = models.CharField(max_length=30, choices=VehicleType.choices)
    vehicle_reg_number = models.CharField(max_length=20, unique=True, db_index=True)
    make_and_model = models.CharField(max_length=100)

    max_weight_kg = models.PositiveIntegerField(
        help_text="Maximum payload weight in Kilograms",
        validators=[MinValueValidator(100)],
    )

    vehicle_front_photo = models.ImageField(upload_to="vehicle/front/")
    vehicle_rear_photo = models.ImageField(upload_to="vehicle/rear/")
    vehicle_side_photo = models.ImageField(upload_to="vehicle/side/")

    completed_trips_count = models.PositiveIntegerField(default=0)
    is_available = models.BooleanField(default=True, db_index=True)

    # Removed invalid max_length=3 for DecimalField
    rating = models.DecimalField(
        max_digits=3,
        decimal_places=2,
        default=5.00,
        validators=[MinValueValidator(0.00), MaxValueValidator(5.00)],
    )

    class Meta:
        verbose_name = "Driver Profile"
        verbose_name_plural = "Driver Profiles"

    def __str__(self):
        return f"Driver Profile: {self.user.email}"
