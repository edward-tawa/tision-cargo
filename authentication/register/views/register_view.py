from django.conf import settings
from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView

from authentication.otp.services.otp_service import OTPService
from core.api_responses.responses import error_response, success_response
from users.serializers.user_serializer import (
    CreateUserSerializer,
    ReadUserSerializer,
)


class RegisterView(APIView):
    """
    Handle user registration, generate an OTP, and return user data and the OTP code upon success.
    """

    permission_classes = [AllowAny]

    @extend_schema(
        request=CreateUserSerializer,
        responses={201: ReadUserSerializer},
        summary="Register a new user",
        description="Creates a new user account, generates an OTP, and returns the profile details and OTP code.",
    )
    def post(self, request):
        serializer = CreateUserSerializer(data=request.data)

        if serializer.is_valid():
            user = serializer.save()

            # Generate and dispatch (log/send) the OTP
            otp_obj = OTPService.generate_and_send_otp(user)

            # Serialize the user using ReadUserSerializer for a clean output representation
            output_serializer = ReadUserSerializer(user)

            response_data = {
                "user": output_serializer.data,
            }

            # Include the code in the response during development/testing
            if settings.DEBUG:
                response_data["otp_code"] = otp_obj.code

            return success_response(
                message="User registered successfully. Use the provided OTP to verify your account.",
                status=status.HTTP_201_CREATED,
                data=response_data,
            )

        return error_response(
            message="Registration failed due to validation errors.",
            status=status.HTTP_400_BAD_REQUEST,
            errors=serializer.errors,
        )
