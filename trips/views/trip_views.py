from rest_framework import status, viewsets
from rest_framework.decorators import action

from core.api_responses.responses import error_response, success_response
from trips.models.trip_model import Trip
from trips.serializers.trip_serializer import TripSerializer
from trips.services.trip_business_service import TripBusinessService
from trips.services.trip_crud_service import TripCRUDService


class TripViewSet(viewsets.GenericViewSet):
    queryset = Trip.objects.all()
    serializer_class = TripSerializer

    def list(self, request):
        trips = TripCRUDService.get_trips(
            client=request.query_params.get("client"),
            driver=request.query_params.get("driver"),
            status=request.query_params.get("status"),
        )
        trips = self.filter_queryset(trips)

        return success_response(
            message="Trips retrieved successfully.",
            data=TripSerializer(trips, many=True).data,
            status=status.HTTP_200_OK,
        )

    def retrieve(self, request, pk=None):
        trip = TripCRUDService.get_trip(trip_id=pk)
        return success_response(
            message="Trip retrieved successfully.",
            data=TripSerializer(trip).data,
            status=status.HTTP_200_OK,
        )

    def create(self, request):
        serializer = TripSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        trip = TripCRUDService.create_trip(**serializer.validated_data)

        return success_response(
            message="Trip created successfully.",
            data=TripSerializer(trip).data,
            status=status.HTTP_201_CREATED,
        )

    def update(self, request, pk=None):
        return self._update_trip(request, pk, partial=False)

    def partial_update(self, request, pk=None):
        return self._update_trip(request, pk, partial=True)

    def _update_trip(self, request, pk, partial):
        trip = TripCRUDService.get_trip(trip_id=pk)
        serializer = TripSerializer(trip, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)

        updated_trip = TripCRUDService.update_trip(
            trip_id=pk, **serializer.validated_data
        )
        return success_response(
            message="Trip updated successfully.",
            data=TripSerializer(updated_trip).data,
            status=status.HTTP_200_OK,
        )

    def destroy(self, request, pk=None):
        TripCRUDService.delete_trip(trip_id=pk)
        return success_response(
            message="Trip deleted successfully.",
            status=status.HTTP_200_OK,
        )

    @action(detail=True, methods=["post"], url_path="update-location")
    def update_location(self, request, pk=None):
        """
        Endpoint for a driver to ping real-time coordinates.
        Payload: { "lat": 12.345678, "lng": 98.765432 }
        """
        lat = request.data.get("lat")
        lng = request.data.get("lng")

        if lat is None or lng is None:
            return error_response(
                message="Both 'lat' and 'lng' are required in the request body.",
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Updated to match TripBusinessService.update_driver_location
        trip = TripBusinessService.update_driver_location(
            trip_id=pk,
            lat=lat,
            lng=lng,
            user=request.user,
        )

        return success_response(
            message="Trip location updated successfully.",
            data=TripSerializer(trip).data,
            status=status.HTTP_200_OK,
        )

    @action(detail=True, methods=["post"], url_path="update-status")
    def update_trip_status(self, request, pk=None):
        """
        Endpoint to advance or update the trip status.
        Payload: { "new_status": "in_transit" }
        """
        # Matches the 'new_status' parameter name in your service method
        new_status = request.data.get("new_status") or request.data.get("trip_status")
        if not new_status:
            return error_response(
                message="'new_status' is required in the request body.",
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Updated to match TripBusinessService.update_trip_status signature
        trip = TripBusinessService.update_trip_status(
            trip_id=pk,
            new_status=new_status,
            user=request.user,
        )

        return success_response(
            message="Trip status updated successfully.",
            data=TripSerializer(trip).data,
            status=status.HTTP_200_OK,
        )
