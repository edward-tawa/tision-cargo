from rest_framework import serializers
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.tokens import RefreshToken


class LogoutSerializer(serializers.Serializer):
    """
    Serializer for user logout requiring a valid refresh token.
    """

    refresh = serializers.CharField(required=True)

    def validate_refresh(self, value):
        try:
            # Verify the token is a valid refresh token structure
            self.token = RefreshToken(value)
        except TokenError:
            raise serializers.ValidationError("Invalid or expired refresh token.")
        return value

    def save(self, **kwargs):
        try:
            # Blacklist the token
            self.token.blacklist()
        except TokenError:
            raise serializers.ValidationError(
                "Token could not be blacklisted (it may already be invalid)."
            )
