# bids/views/driver_bid_application_views.py
from loguru import logger
from rest_framework import status, viewsets

from bids.models.driver_bid_application_model import DriverBidApplication
from bids.serializers.driver_bid_application_serializer import (
    DriverBidApplicationSerializer,
)
from bids.services.driver_bid_application_service import (
    DriverBidApplicationCRUDService,
)
from core.api_responses.responses import success_response


class DriverBidApplicationViewSet(viewsets.GenericViewSet):
    queryset = DriverBidApplication.objects.all()
    serializer_class = DriverBidApplicationSerializer

    def list(self, request):
        logger.info("Fetching list of driver bid applications.")
        applications = DriverBidApplicationCRUDService.get_bid_applications(
            bid_id=request.query_params.get("bid"),
            driver_id=request.query_params.get("driver"),
            status_val=request.query_params.get("status"),
        )
        applications = self.filter_queryset(applications)

        return success_response(
            message="Driver applications retrieved successfully.",
            data=DriverBidApplicationSerializer(applications, many=True).data,
            status=status.HTTP_200_OK,
        )

    def retrieve(self, request, pk=None):
        logger.info(f"Fetching driver application with ID: {pk}")
        application = DriverBidApplicationCRUDService.get_bid_application_by_id(
            bid_application_id=pk
        )

        return success_response(
            message="Driver application retrieved successfully.",
            data=DriverBidApplicationSerializer(application).data,
            status=status.HTTP_200_OK,
        )

    def create(self, request):
        logger.info("Attempting to create a new driver application.")
        serializer = DriverBidApplicationSerializer(
            data=request.data, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)

        application = DriverBidApplicationCRUDService.create_driver_bid_application(
            **serializer.validated_data
        )

        return success_response(
            message="Driver application created successfully.",
            data=DriverBidApplicationSerializer(application).data,
            status=status.HTTP_201_CREATED,
        )

    def update(self, request, pk=None):
        return self._update_application(request, pk, partial=False)

    def partial_update(self, request, pk=None):
        return self._update_application(request, pk, partial=True)

    def _update_application(self, request, pk, partial):
        logger.info(
            f"{'Partial' if partial else 'Full'} updating driver application ID: {pk}"
        )

        # Verify application exists before binding data to serializer
        application = DriverBidApplicationCRUDService.get_bid_application_by_id(
            bid_application_id=pk
        )

        serializer = DriverBidApplicationSerializer(
            application,
            data=request.data,
            partial=partial,
            context={"request": request},
        )
        serializer.is_valid(raise_exception=True)

        updated_application = (
            DriverBidApplicationCRUDService.update_driver_bid_application(
                application_id=pk, **serializer.validated_data
            )
        )

        return success_response(
            message="Driver application updated successfully.",
            data=DriverBidApplicationSerializer(updated_application).data,
            status=status.HTTP_200_OK,
        )

    def destroy(self, request, pk=None):
        logger.warning(f"Deleting driver application ID: {pk}")
        DriverBidApplicationCRUDService.delete_driver_bid_application(application_id=pk)

        return success_response(
            message="Driver application deleted successfully.",
            status=status.HTTP_200_OK,
        )
