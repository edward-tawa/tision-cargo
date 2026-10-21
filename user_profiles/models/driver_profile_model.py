from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from core.models.time_stamp_model import TimeStampModel


class DriverProfile(TimeStampModel):
    """
    Profile model for system drivers, equipped with a dedicated UUID primary key.
    """

    class VehicleType(models.TextChoices):
        PICKUP = "PICKUP", "Pickup truck 1 tonne"
        TRUCK_3T = "3_TONNE", "3 Tonne truck"
        TRUCK_5T = "5_TONNE", "5 Tonne truck"
        TRUCK_7T = "7_TONNE", "7 Tonne truck"
        TIPPER = "TIPPER", "Tipper truck"

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
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

    rating = models.DecimalField(
        max_digits=3,
        decimal_places=2,
        default=5.00,
        validators=[MinValueValidator(0.00), MaxValueValidator(5.00)],
    )

    class Meta:
        verbose_name = "Driver Profile"
        verbose_name_plural = "Driver Profiles"
        permissions = [
            ("can_create_driver_profile", "Can create a driver profile"),
            ("can_read_driver_profile", "Can read a driver profile"),
            ("can_update_driver_profile", "Can update a driver profile"),
            ("can_delete_driver_profile", "Can delete a driver profile"),
        ]

    def __str__(self):
        return f"Driver Profile: {self.user.email}"
