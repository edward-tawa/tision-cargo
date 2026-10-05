from rest_framework import status
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from authentication.login.serializers.login_serializer import LoginSerializer
from core.api_responses.responses import error_response, success_response
from users.models.user_model import CustomUser


class LoginView(APIView):
    """
    A view for user login supporting either email or phone number.
    """

    serializer_class = LoginSerializer

    def post(self, request):
        serializer = LoginSerializer(data=request.data)

        if not serializer.is_valid():
            return error_response(
                message="Invalid input data.",
                status=status.HTTP_400_BAD_REQUEST,
                errors=serializer.errors,
            )

        # Extract validated data
        email = serializer.validated_data.get("email")
        phone_number = serializer.validated_data.get("phone_number")
        password = serializer.validated_data.get("password")

        # Step 1: Find the user by email or phone number
        user = None
        if email:
            user = CustomUser.objects.filter(email__iexact=email).first()
        elif phone_number:
            user = CustomUser.objects.filter(phone_number=phone_number).first()

        # Step 2: Verify user exists and password is correct
        if user is not None and user.check_password(password):
            # Optional: Ensure the user's status allows login (e.g., must be verified)
            if user.status != CustomUser.STATUS.VERIFIED:
                return error_response(
                    message="Your account is pending verification or suspended.",
                    status=status.HTTP_403_FORBIDDEN,
                )

            # Generate JWT tokens
            refresh = RefreshToken.for_user(user)

            response_data = {
                "user": {
                    "id": user.id,
                    "email": user.email,
                    "first_name": user.first_name,
                    "last_name": user.last_name,
                    "age": user.age,
                    "phone_number": str(user.phone_number),
                    "role": user.role,
                    "status": user.status,
                },
                "tokens": {
                    "refresh": str(refresh),
                    "access": str(refresh.access_token),
                },
            }

            return success_response(
                message="Login successful.",
                status=status.HTTP_200_OK,
                data=response_data,
            )

        # Authentication failed
        return error_response(
            message="Invalid credentials. Please check your email/phone number and password.",
            status=status.HTTP_401_UNAUTHORIZED,
        )
