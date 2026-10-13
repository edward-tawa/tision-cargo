from rest_framework import status, viewsets
from rest_framework.decorators import action

from bookings.models.booking_model import Booking
from bookings.serializers.booking_serializer import BookingSerializer
from bookings.services.booking_business_service import BookingBusinessService
from bookings.services.booking_crud_service import BookingCRUDService
from core.api_responses.responses import error_response, success_response


class BookingViewSet(viewsets.GenericViewSet):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer

    def list(self, request):
        bookings = BookingCRUDService.get_bookings(
            client=request.query_params.get("client"),
            assigned_driver=request.query_params.get("assigned_driver"),
            booking_status=request.query_params.get("booking_status"),
        )
        bookings = self.filter_queryset(bookings)

        return success_response(
            message="Bookings retrieved successfully.",
            data=BookingSerializer(bookings, many=True).data,
            status=status.HTTP_200_OK,
        )

    def retrieve(self, request, pk=None):
        booking = BookingCRUDService.get_booking(booking_id=pk)
        return success_response(
            message="Booking retrieved successfully.",
            data=BookingSerializer(booking).data,
            status=status.HTTP_200_OK,
        )

    def create(self, request):
        serializer = BookingSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        validated_data = serializer.validated_data
        client = validated_data.get("client") or (
            request.user if request.user.is_authenticated else None
        )

        booking = BookingBusinessService.create_booking_for_client(
            client=client,
            **validated_data,
        )

        return success_response(
            message="Booking created successfully.",
            data=BookingSerializer(booking).data,
            status=status.HTTP_201_CREATED,
        )

    def update(self, request, pk=None):
        return self._update_booking(request, pk, partial=False)

    def partial_update(self, request, pk=None):
        return self._update_booking(request, pk, partial=True)

    def _update_booking(self, request, pk, partial):
        booking = BookingCRUDService.get_booking(booking_id=pk)
        serializer = BookingSerializer(booking, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)

        updated_booking = BookingCRUDService.update_booking(
            booking_id=pk, **serializer.validated_data
        )
        return success_response(
            message="Booking updated successfully.",
            data=BookingSerializer(updated_booking).data,
            status=status.HTTP_200_OK,
        )

    def destroy(self, request, pk=None):
        BookingCRUDService.delete_booking(booking_id=pk)
        return success_response(
            message="Booking deleted successfully.",
            status=status.HTTP_200_OK,
        )

    @action(detail=True, methods=["post"], url_path="accept-bid")
    def accept_bid(self, request, pk=None):
        """
        Endpoint for a client to accept a specific driver's bid.
        Payload: { "bid_id": 123 }
        """
        bid_id = request.data.get("bid_id")
        if not bid_id:
            return error_response(
                message="'bid_id' is required in the request body.",
                status=status.HTTP_400_BAD_REQUEST,
            )

        booking = BookingBusinessService.accept_driver_bid(
            booking_id=pk,
            bid_id=bid_id,
            user=request.user,
        )

        return success_response(
            message="Driver bid accepted successfully. Job assigned and trip created.",
            data=BookingSerializer(booking).data,
            status=status.HTTP_200_OK,
        )

    @action(detail=True, methods=["post"], url_path="cancel")
    def cancel_booking(self, request, pk=None):
        """
        Endpoint for a client to cancel a booking.
        """
        booking = BookingBusinessService.cancel_booking(
            booking_id=pk, user=request.user
        )

        return success_response(
            message="Booking cancelled successfully.",
            data=BookingSerializer(booking).data,
            status=status.HTTP_200_OK,
        )
