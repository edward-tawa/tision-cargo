from rest_framework import status, viewsets
from rest_framework.decorators import action

from bids.models.bid_model import Bid
from bids.serializers.bid_serializer import BidSerializer
from bids.services.bid_business_service import BidBusinessService
from bids.services.bid_crud_service import BidCRUDService
from core.api_responses.responses import success_response


class BidViewSet(viewsets.GenericViewSet):
    queryset = Bid.objects.all()
    serializer_class = BidSerializer

    def list(self, request):
        """
        Retrieve a list of bids, optionally filtered by booking, driver, or bid status.
        """
        bids = BidCRUDService.get_bids(
            booking=request.query_params.get("booking"),
            driver=request.query_params.get("driver"),
            bid_status=request.query_params.get("bid_status"),
        )
        bids = self.filter_queryset(bids)

        return success_response(
            message="Bids retrieved successfully.",
            data=BidSerializer(bids, many=True).data,
            status=status.HTTP_200_OK,
        )

    def retrieve(self, request, pk=None):
        """
        Retrieve a single bid by its ID.
        """
        bid = BidCRUDService.get_bid(bid_id=pk)
        return success_response(
            message="Bid retrieved successfully.",
            data=BidSerializer(bid).data,
            status=status.HTTP_200_OK,
        )

    def create(self, request):
        """
        Allows a driver to submit a new price offer (bid) for a booking.
        Payload: { "booking_id": 1, "bid_amount": 350.00, "driver_notes": "..." }
        """
        serializer = BidSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        validated_data = serializer.validated_data
        booking_id = request.data.get("booking_id") or (
            validated_data.get("booking").id if validated_data.get("booking") else None
        )

        bid = BidBusinessService.create_bid_for_driver(
            booking_id=booking_id,
            driver=request.user,
            bid_amount=validated_data.get("bid_amount"),
            driver_notes=validated_data.get("driver_notes", ""),
        )

        return success_response(
            message="Bid submitted successfully.",
            data=BidSerializer(bid).data,
            status=status.HTTP_201_CREATED,
        )

    def update(self, request, pk=None):
        return self._update_bid(request, pk, partial=False)

    def partial_update(self, request, pk=None):
        return self._update_bid(request, pk, partial=True)

    def _update_bid(self, request, pk, partial):
        """
        Allows a driver to update their pending bid details.
        """
        serializer = BidSerializer(data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)

        validated_data = serializer.validated_data

        updated_bid = BidBusinessService.update_bid_by_driver(
            bid_id=pk,
            driver=request.user,
            bid_amount=validated_data.get("bid_amount"),
            driver_notes=validated_data.get("driver_notes"),
        )

        return success_response(
            message="Bid updated successfully.",
            data=BidSerializer(updated_bid).data,
            status=status.HTTP_200_OK,
        )

    def destroy(self, request, pk=None):
        """
        Delete a bid record.
        """
        BidCRUDService.delete_bid(bid_id=pk)
        return success_response(
            message="Bid deleted successfully.",
            status=status.HTTP_200_OK,
        )

    @action(detail=True, methods=["post"], url_path="cancel")
    def cancel_bid(self, request, pk=None):
        """
        Endpoint for a driver to cancel/withdraw their pending bid.
        """
        bid = BidBusinessService.cancel_bid_by_driver(
            bid_id=pk,
            driver=request.user,
        )

        return success_response(
            message="Bid cancelled successfully.",
            data=BidSerializer(bid).data,
            status=status.HTTP_200_OK,
        )
