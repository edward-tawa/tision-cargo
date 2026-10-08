from rest_framework import serializers

from authentication.otp.models.otp_model import OTP
from users.models.user_model import CustomUser


class VerifyOTPSerializer(serializers.Serializer):
    phone_number = serializers.CharField(required=True)
    code = serializers.CharField(max_length=6, min_length=6, required=True)

    def validate(self, attrs):
        phone_number = attrs.get("phone_number")
        code = attrs.get("code")

        try:
            user = CustomUser.objects.get(phone_number=phone_number)
        except CustomUser.DoesNotExist:
            raise serializers.ValidationError(
                {"phone_number": ["User with this phone number does not exist."]}
            )

        if user.status == CustomUser.STATUS.VERIFIED:
            raise serializers.ValidationError(
                {"non_field_errors": ["This account is already verified."]}
            )

        try:
            otp_obj = OTP.objects.get(user=user, code=code, is_used=False)
        except OTP.DoesNotExist:
            raise serializers.ValidationError(
                {"code": ["Invalid or already used verification code."]}
            )

        if otp_obj.is_expired:
            raise serializers.ValidationError(
                {"code": ["This verification code has expired."]}
            )

        attrs["user"] = user
        attrs["otp_obj"] = otp_obj
        return attrs
