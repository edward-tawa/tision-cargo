from rest_framework import status
from rest_framework.views import APIView
from rest_framework_simplejwt.serializers import TokenRefreshSerializer

from core.api_responses.responses import error_response, success_response


class CustomTokenRefreshView(APIView):
    """
    A view to refresh JWT access tokens using a valid refresh token,
    formatted with your custom response structure.
    """

    serializer_class = TokenRefreshSerializer

    def post(self, request):
        serializer = TokenRefreshSerializer(data=request.data)

        if serializer.is_valid():
            return success_response(
                message="Token refreshed successfully.",
                status=status.HTTP_200_OK,
                data=serializer.validated_data,
            )

        return error_response(
            message="Token refresh failed.",
            status=status.HTTP_400_BAD_REQUEST,
            errors=serializer.errors,
        )
