from rest_framework import serializers

from users.models.user_model import CustomUser


class RequestOTPSerializer(serializers.Serializer):
    phone_number = serializers.CharField(required=True)

    def validate(self, attrs):
        phone_number = attrs.get("phone_number")

        try:
            user = CustomUser.objects.get(phone_number=phone_number)
        except CustomUser.DoesNotExist:
            raise serializers.ValidationError(
                {"phone_number": ["User with this phone number does not exist."]}
            )

        if user.status == CustomUser.STATUS.VERIFIED:
            raise serializers.ValidationError(
                {
                    "non_field_errors": [
                        "This account is already verified. Please log in."
                    ]
                }
            )

        attrs["user"] = user
        return attrs
