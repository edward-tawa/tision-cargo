from django.conf import settings
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError


class CustomJWTAuthentication(JWTAuthentication):
    """
    Custom JWT authentication class that extends the default JWTAuthentication to authenticate token
    """

    def authenticate(self, request):
        """
        Override the authenticate method to customize the authentication process.
        """
        cookie_name = settings.SIMPLE_JWT.get("ACCESS_COOKIE", "access_token")
        token = request.COOKIES.get(cookie_name)

        if token is None:
            return None

        try:
            validated_token = self.get_validated_token(token)
            user = self.get_user(validated_token)
        except (InvalidToken, TokenError):
            return None

        return (user, validated_token)
