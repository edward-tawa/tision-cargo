from phonenumber_field.serializerfields import PhoneNumberField
from rest_framework import serializers


class LoginSerializer(serializers.Serializer):
    """
    Serializer for user login allowing either email or phone number.
    """

    email = serializers.EmailField(required=False, allow_blank=True)
    password = serializers.CharField(write_only=True, required=True)
    phone_number = PhoneNumberField(required=False, allow_blank=True)

    def validate(self, attrs):
        email = attrs.get("email")
        phone_number = attrs.get("phone_number")

        # Ensure at least one identifier is provided
        if not email and not phone_number:
            raise serializers.ValidationError(
                {
                    "detail": "You must provide either an email or a phone number to log in."
                }
            )

        return attrs
