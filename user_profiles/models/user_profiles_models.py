from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


class DriverProfile(models.Model):
    """
    Profile model for system drivers.
    Primary key is explicitly inherited from the Common User model.
    """

    VEHICLE_CHOICES = [
        ("motorcycle", "Motorcycle"),
        ("van", "Cargo Van"),
        ("rigid_truck", "Rigid Truck"),
        ("articulated_truck", "Articulated Truck"),
    ]

    # primary_key=True makes this field the actual PK of this table, matching the User's ID
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        primary_key=True,
        related_name="driver_profile",
    )
    license_number = models.CharField(max_length=50, unique=True, db_index=True)
    vehicle_type = models.CharField(max_length=30, choices=VEHICLE_CHOICES)
    is_available = models.BooleanField(default=True, db_index=True)
    rating = models.DecimalField(
        max_length=3,
        max_digits=3,
        decimal_places=2,
        default=5.00,
        validators=[MinValueValidator(0.00), MaxValueValidator(5.00)],
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Driver Profile"
        verbose_name_plural = "Driver Profiles"

    def __str__(self):
        return f"Driver Profile: {self.user.email if hasattr(self.user, 'email') else self.user.username}"


class ClientProfile(models.Model):
    """
    Profile model for clients who book haulage services.
    Primary key is explicitly inherited from the Common User model.
    """

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        primary_key=True,
        related_name="client_profile",
    )
    company_name = models.CharField(max_length=150, blank=True, null=True)
    home_address = models.TextField()
    phone_number = models.CharField(max_length=20, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Client Profile"
        verbose_name_plural = "Client Profiles"

    def __str__(self):
        return f"Client Profile: {self.company_name or (self.user.email if hasattr(self.user, 'email') else self.user.username)}"
