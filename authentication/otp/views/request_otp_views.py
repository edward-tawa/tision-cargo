from django.conf import settings
from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView

from authentication.otp.serializers.request_otp_serializer import RequestOTPSerializer
from authentication.otp.services.otp_service import OTPService
from core.api_responses.responses import error_response, success_response


class RequestOTPView(APIView):
    """
    Generates and sends a new OTP via SMS for pending accounts.
    """

    permission_classes = [AllowAny]

    @extend_schema(
        request=RequestOTPSerializer,
        summary="Request a new OTP",
        description="Submits a phone number to generate and dispatch a fresh 6-digit OTP code.",
    )
    def post(self, request):
        serializer = RequestOTPSerializer(data=request.data)

        if serializer.is_valid():
            user = serializer.validated_data["user"]

            # Generate and dispatch new OTP, capturing the returned OTP object
            otp_obj = OTPService.generate_and_send_otp(user)

            response_data = None
            if settings.DEBUG:
                response_data = {"otp_code": otp_obj.code}

            return success_response(
                message="A new verification code has been sent to your phone.",
                status=status.HTTP_200_OK,
                data=response_data,
            )

        return error_response(
            message="Failed to request OTP.",
            status=status.HTTP_400_BAD_REQUEST,
            errors=serializer.errors,
        )
