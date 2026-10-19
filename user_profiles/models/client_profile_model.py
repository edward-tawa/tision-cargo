from django.conf import settings
from django.db import models

from core.models.time_stamp_model import TimeStampModel


class ClientProfile(TimeStampModel):
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

    # Optional: Great if your haulage service handles business-to-business (B2B) clients
    company_name = models.CharField(max_length=150, blank=True)

    # Generalized address for pickup/billing reference
    default_address = models.TextField(
        blank=True, help_text="Default address for pickup or billing reference."
    )

    class Meta:
        verbose_name = "Client Profile"
        verbose_name_plural = "Client Profiles"
        permissions = [
            ("can_create_client_profile", "Can create a client profile"),
            ("can_read_client_profile", "Can read a client profile"),
            ("can_update_client_profile", "Can update a client profile"),
            ("can_delete_client_profile", "Can delete a client profile"),
        ]

    def __str__(self):
        return f"Client Profile: {self.user.email}"
