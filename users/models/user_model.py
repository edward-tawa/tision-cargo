from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from django.db import models
from django.utils.translation import gettext_lazy as _
from phonenumber_field.modelfields import PhoneNumberField

from core.models.time_stamp_model import TimeStampModel


class CustomUserManager(BaseUserManager):
    """Custom user manager to handle user creation and management."""

    def create_user(self, email, password=None, **extra_fields):
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
        extra_fields.setdefault("status", CustomUser.STATUS.VERIFIED)
        extra_fields.setdefault("role", CustomUser.ROLE.ADMIN)

        if extra_fields.get("is_staff") is not True:
            raise ValueError(_("Superuser must have is_staff=True."))
        if extra_fields.get("is_superuser") is not True:
            raise ValueError(_("Superuser must have is_superuser=True."))

        return self.create_user(email, password, **extra_fields)


class CustomUser(AbstractBaseUser, PermissionsMixin, TimeStampModel):
    """Custom user model that uses email as the unique identifier instead of username."""

    class ROLE(models.TextChoices):
        ADMIN = "admin", _("Admin")
        CLIENT = "client", _("Client")
        DRIVER = "driver", _("Driver")

    class STATUS(models.TextChoices):
        SUSPENDED = "suspended", _("Suspended")
        PENDING = "pending", _("Pending")
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

    age = models.PositiveSmallIntegerField(_("age"), help_text=_("Enter your age."))

    phone_number = PhoneNumberField(
        _("phone number"),
        unique=True,
        help_text=_("Required. Enter your phone number."),
    )

    role = models.CharField(
        _("role"),
        max_length=20,
        choices=ROLE.choices,
        default=ROLE.CLIENT,
        help_text=_(
            "Required. Select the role of the user (Admin, Client, or Driver)."
        ),
    )
    status = models.CharField(
        _("status"),
        max_length=20,
        choices=STATUS.choices,
        default=STATUS.PENDING,
        help_text=_(
            "Required. Select the status of the user (Suspended or Verified or Pending)."
        ),
    )
    is_staff = models.BooleanField(
        _("staff status"),
        default=False,
        help_text=_("Designates whether the user can log into this admin site."),
    )

    objects = CustomUserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = [
        "phone_number",
        "age",
    ]

    class Meta:
        verbose_name = _("user")
        verbose_name_plural = _("users")
        ordering = ["email"]
        permissions = [
            ("can_suspend_user", _("Can suspend user")),
            ("can_verify_user", _("Can verify user")),
            ("can_change_user_role", _("Can change user role")),
            ("can_change_user_status", _("Can change user status")),
            ("can_change_user_password", _("Can change user password")),
            ("can_change_user_email", _("Can change user email")),
            ("can_change_user_phone_number", _("Can change user phone number")),
            ("can_change_user_age", _("Can change user age")),
            ("can_create_bid", _("Can create bid")),
            ("can_accept_bid", _("Can accept bid")),
            ("can_reject_bid", _("Can reject bid")),
            ("can_cancel_bid", _("Can cancel bid")),
            ("can_complete_bid", _("Can complete bid")),
        ]

    def __str__(self):
        """Return a string representation of the user."""
        return f"{self.email} {self.first_name} {self.last_name}"

    @property
    def is_active(self):
        """Return whether the user is active."""
        return self.status == self.STATUS.VERIFIED
