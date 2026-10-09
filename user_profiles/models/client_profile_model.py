from django.conf import settings
from django.db import models


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
    home_address = models.TextField()
    phone_number = models.CharField(max_length=20, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Client Profile"
        verbose_name_plural = "Client Profiles"

    def __str__(self):
        return f"Client Profile: {(self.user.email if hasattr(self.user, 'email') else self.user.username)}"
