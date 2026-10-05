from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from users.serializers.user_serializers import UserCreateSerializer

from core.api_responses.responses import error_response, success_response


class RegisterView(APIView):
    """
    Handle user registration and return JWT tokens upon success using standard response wrappers.
    """

    permission_classes = [AllowAny]

    def post(self, request):
        serializer = UserCreateSerializer(data=request.data)

        if serializer.is_valid():
            user = serializer.save()

            # Generate JWT tokens for the newly registered user
            refresh = RefreshToken.for_user(user)

            # Package user data and tokens together for the response data
            response_data = {
                "user": serializer.data,
                "tokens": {
                    "refresh": str(refresh),
                    "access": str(refresh.access_token),
                },
            }

            return success_response(
                message="User registered successfully.",
                status=status.HTTP_201_CREATED,
                data=response_data,
            )

        # Return validation errors neatly using your error wrapper
        return error_response(
            message="Registration failed due to validation errors.",
            status=status.HTTP_400_BAD_REQUEST,
            errors=serializer.errors,
        )
