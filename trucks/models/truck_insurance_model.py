import uuid

from django.core.validators import MinValueValidator
from django.db import models

from trucks.models.truck_model import Truck


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
