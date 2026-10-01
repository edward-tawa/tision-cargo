from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers

from users.models.user_model import CustomUser

MIN_AGE = 18


def _validate_age(value):
    if value < MIN_AGE:
        raise serializers.ValidationError(f"Age must be at least {MIN_AGE}.")
    return value


class UserReadSerializer(serializers.ModelSerializer):
    """Output only. Never used for input."""

    class Meta:
        model = CustomUser
        fields = [
            "id",
            "email",
            "first_name",
            "last_name",
            "age",
            "phone_number",
            "role",
            "status",
        ]
        read_only_fields = fields


class UserCreateSerializer(serializers.ModelSerializer):
    """Validates input for registration. Role and status use model defaults."""

    email = serializers.EmailField(required=True)
    password = serializers.CharField(write_only=True, style={"input_type": "password"})

    class Meta:
        model = CustomUser
        fields = [
            "email",
            "password",
            "first_name",
            "last_name",
            "age",
            "phone_number",
        ]

    def validate_email(self, value):
        if CustomUser.objects.filter(email__iexact=value).exists():
            raise serializers.ValidationError("A user with this email already exists.")
        return value

    def validate_password(self, value):
        validate_password(value)
        return value

    def validate_age(self, value):
        return _validate_age(value)


class UserUpdateSerializer(serializers.ModelSerializer):
    """Profile fields only. No email, password, role or status."""

    class Meta:
        model = CustomUser
        fields = ["first_name", "last_name", "age", "phone_number"]

    def validate_age(self, value):
        return _validate_age(value)
