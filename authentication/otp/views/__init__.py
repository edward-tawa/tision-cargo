from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView

from authentication.otp.serializers.verify_otp_serializer import VerifyOTPSerializer
from core.api_responses.responses import error_response, success_response
from users.models.user_model import CustomUser
from users.serializers.user_serializer import ReadUserSerializer


class VerifyOTPView(APIView):
    """
    Verify user account via phone number and OTP, updating status to verified.
    Tokens are issued separately upon login.
    """

    permission_classes = [AllowAny]

    @extend_schema(
        request=VerifyOTPSerializer,
        summary="Verify account OTP",
        description="Submits the phone number and 6-digit OTP to activate the account. Please use the login endpoint to receive JWT tokens afterwards.",
    )
    def post(self, request):
        serializer = VerifyOTPSerializer(data=request.data)

        if serializer.is_valid():
            user = serializer.validated_data["user"]
            otp_obj = serializer.validated_data["otp_obj"]

            # Mark OTP as used so it cannot be replayed
            otp_obj.is_used = True
            otp_obj.save()

            # Update user status to verified
            user.status = CustomUser.STATUS.VERIFIED
            user.save()

            user_data = ReadUserSerializer(user).data

            response_data = {
                "user": user_data,
            }

            return success_response(
                message="Account verified successfully. Please proceed to login.",
                status=status.HTTP_200_OK,
                data=response_data,
            )

        return error_response(
            message="Verification failed due to validation errors.",
            status=status.HTTP_400_BAD_REQUEST,
            errors=serializer.errors,
        )
