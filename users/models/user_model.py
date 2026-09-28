from django.contrib.auht.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.db import models
from django.utils.translation import gettext_lazy as _

from core.models.time_stamp_model import TimeStampModel


class CustomUserManager(models.Manager):
    """Custom user manager to handle user creation and management."""

    def create_user(self, email, password, **extra_fields):
        """Create and save a regular user with the given email and password."""
        if not email:
            raise ValueError(_("The Email field must be set"))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, **extra_fields):
        """Create and save a superuser with the given email and password."""
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError(_("Superuser must have is_staff=True."))
        if extra_fields.get("is_superuser") is not True:
            raise ValueError(_("Superuser must have is_superuser=True."))

        return self.create_user(email, password, **extra_fields)


class CustomUser(AbstractBaseUser, PermissionsMixin, TimeStampModel):
    """Custom user model that uses email as the unique identifier instead of username."""

    class UserRole(models.TextChoices):
        ADMIN = "admin", _("Admin")
        USER = "client", _("Client")
        DRIVER = "driver", _("Driver")

    class STATUS(models.TextChoices):
        SUSPENDED = "suspended", _("Suspended")
        VERIFIED = "verified", _("Verified")

    email = models.EmailField(
        _("email address"),
        unique=True,
        help_text=_("Required. Enter a valid email address."),
    )
    first_name = models.CharField(
        _("first name"),
        max_length=150,
        blank=True,
        help_text=_("Optional. Enter your first name."),
    )
    last_name = models.CharField(
        _("last name"),
        max_length=150,
        blank=True,
        help_text=_("Optional. Enter your last name."),
    )
    age = models.IntegerField(
        _("age"), max_length=150, help_text=_("Optional. Enter your age.")
    )

    phone_number = models.CharField(
        _("phone number"),
        max_length=20,
        help_text=_("Required. Enter your phone number."),
    )
    password = models.CharField(
        _("password"), max_length=128, help_text=_("Required. Enter a secure password.")
    )

    role = models.CharField(
        _("role"),
        max_length=20,
        choices=UserRole.choices,
        default=UserRole.USER,
        help_text=_(
            "Required. Select the role of the user (Admin, Client, or Driver)."
        ),
    )
    status = models.CharField(
        _("status"),
        max_length=20,
        choices=STATUS.choices,
        default=STATUS.ACTIVE,
        help_text=_("Required. Select the status of the user (Suspended or Verified)."),
    )
    is_staff = models.BooleanField(
        _("staff status"),
        default=False,
        help_text=_("Designates whether the user can log into this admin site."),
    )
    is_active = models.BooleanField(
        _("active"),
        default=True,
        help_text=_(
            "Designates whether this user should be treated as active. Unselect this instead of deleting accounts."
        ),
    )
    created_at = models.DateTimeField(
        _("created at"),
        auto_now_add=True,
        help_text=_("The date and time when the user account was created."),
    )
    updated_at = models.DateTimeField(
        _("updated at"),
        auto_now=True,
        help_text=_("The date and time when the user account was last updated."),
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = [
        "is_staff",
        "is_active",
        "id_number",
        "phone_number",
        "role",
        "age",
    ]
