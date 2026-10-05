from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from authentication.logout.serializers.logout_serializer import LogoutSerializer
from core.api_responses.responses import error_response, success_response


class LogoutView(APIView):
    """
    A view for user logout that invalidates the refresh token.
    """

    permission_classes = [IsAuthenticated]
    serializer_class = LogoutSerializer

    def post(self, request):
        serializer = LogoutSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return success_response(
                message="User logged out successfully.",
                status=status.HTTP_200_OK,
            )

        return error_response(
            message="Logout failed.",
            status=status.HTTP_400_BAD_REQUEST,
            errors=serializer.errors,
        )
